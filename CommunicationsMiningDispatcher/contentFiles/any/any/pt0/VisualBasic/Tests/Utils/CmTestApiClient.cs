using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using CommunicationsMiningDispatcher.Tests.Resources;

namespace CommunicationsMiningDispatcher.Tests.Utils
{

    public static class StringUtils
    {
        public static string ToSnakeCase(this string str)
        {
            return string.Concat(str.Select((x, i) => i > 0 && char.IsUpper(x) ? "_" + x.ToString() : x.ToString())).ToLower();
        }
    }

    public class SnakeCaseNamingPolicy : JsonNamingPolicy
    {
        public static SnakeCaseNamingPolicy Instance { get; } = new SnakeCaseNamingPolicy();

        public override string ConvertName(string name)
        {
            return name.ToSnakeCase();
        }
    }

    public class CmTestApiClient
    {
        private const string STREAMS_URL = "api/v1/datasets/{0}/{1}/streams";
        private const string SOURCE_URL = "api/v1/sources/{0}/{1}";
        private const string DATASET_URL = "api/v1/datasets/{0}/{1}";
        private readonly JsonSerializerOptions SERIALIZER_OPTIONS = new()
        {
            PropertyNamingPolicy = new SnakeCaseNamingPolicy()
        };

        private readonly HttpClient _client;

        public CmTestApiClient(Uri baseUrl, SecureString apiToken)
        {
            _client = new HttpClient { BaseAddress = baseUrl };
            _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue(
                "Bearer",
                new System.Net.NetworkCredential(string.Empty, apiToken).Password
            );
            _client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json")
            );
        }

        private StringContent SerializeBody(object body)
        {

            var input = JsonSerializer.Serialize(body, SERIALIZER_OPTIONS);
            return new StringContent(input, Encoding.UTF8, mediaType: "application/json");
        }

        private async Task<T> Put<T>(string requestUri, object requestBody, CancellationToken token)
        {
            var content = SerializeBody(requestBody);
            var response = await _client.PutAsync(requestUri, content, token);
            return await ParseApiResponse<T>(response, token);
        }

        private async Task<T> Post<T>(
            string requestUri,
            object requestBody,
            CancellationToken token
        )
        {
            var content = SerializeBody(requestBody);
            var response = await _client.PostAsync(requestUri, content, token);

            return await ParseApiResponse<T>(response, token);
        }

        private async Task<T> ParseApiResponse<T>(
            HttpResponseMessage response,
            CancellationToken token
        )
        {
            if (!response.IsSuccessStatusCode)
            {
                try
                {
                    var response_content = await response.Content.ReadAsStringAsync(token);
                    ErrorResponse error_response = JsonSerializer.Deserialize<ErrorResponse>(
                        response_content
                    );
                    throw new Exception(
                        String.Format(
                            "{0} status code when calling CM API\n\n{1}\n\n{2}",
                            response.StatusCode,
                            error_response.Message,
                            error_response.Path.IsNullOrEmpty() ? "" : error_response.Path
                        )
                    );
                }
                catch (JsonException)
                {
                    throw new Exception(
                        String.Format(
                            "{0} status code when calling CM API. Check base url is correct and ends with '/'",
                            response.StatusCode
                        )
                    );
                }
            }
            response.EnsureSuccessStatusCode();

            String response_as_string = await response.Content.ReadAsStringAsync(token);
            return JsonSerializer.Deserialize<T>(response_as_string, SERIALIZER_OPTIONS);
        }

        public async Task<CreateSourceResponse> CreateSource(
            TestProject project,
            String source_name,
            CreateSourceRequest source,
            CancellationToken token
        )
        {
            return await Put<CreateSourceResponse>(
                GetSourceUrl(project, source_name),
                source,
                token
            );
        }

        public async Task<CreateDatasetResponse> CreateDataset(
            TestProject project,
            String dataset_name,
            CreateDatasetRequest dataset,
            CancellationToken token
        )
        {
            return await Put<CreateDatasetResponse>(
                string.Format(DATASET_URL, project.Name, dataset_name),
                dataset,
                token
            );
        }

        private String GetSourceUrl(TestProject project, String source_name)
        {
            return string.Format(SOURCE_URL, project.Name, source_name);
        }

        public async Task<SyncCommentsResponse> SyncComments(
            TestSource source,
            SyncCommentsRequest comments,
            CancellationToken token
        )
        {
            return await Post<SyncCommentsResponse>(
                String.Format("{0}/sync", GetSourceUrl(source.Project, source.Name)),
                comments,
                token
            );
        }

        public async Task<CreateStreamResponse> CreateStream(
            TestDataset dataset,
            CreateStreamRequest stream,
            CancellationToken token
        )
        {
            return await Put<CreateStreamResponse>(GetStreamsUrl(dataset), stream, token);
        }

        private String GetStreamsUrl(TestDataset dataset)
        {
            return String.Format(STREAMS_URL, dataset.Project.Name, dataset.Name);
        }


        public async Task<FetchStreamResponse> FetchStream(
            TestStream stream,
            FetchStreamRequest request,
            CancellationToken token
        )
        {
            return await Post<FetchStreamResponse>(
                String.Format("{0}/{1}/fetch", GetStreamsUrl(stream.Dataset), stream.Name),
                request,
                token
            );
        }
    }
}

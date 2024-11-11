using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Security;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using CommunicationsMiningDispatcher.Tests.Resources;
using CommunicationsMiningDispatcher.Tests.Utils;
using UiPath.Core.Activities.API;

namespace CommunicationsMiningDispatcher.Tests
{
    using OneOfFilter = Dictionary<String, List<String>>;

    public class CmTestEnvironment
    {
        private const string CM_API_TOKEN_ASSET_NAME = "CmTestingApiToken";
        private const string CM_API_BASE_URL_ASSET_NAME = "CmTestingBaseUrl";
        private const string CM_TEST_PROJECT_ASSET_NAME = "CmTestingProjectName";
        private const string CM_SUPPRESS_BILLING_CONFIRMATION_ASSET_NAME =
            "CmTestingSuppressBillingConfirmation";

        private readonly string _project_name;
        private readonly CancellationTokenSource _ct_source;
        private readonly bool _suppress_billing_confirmation;

        private readonly CmTestApiClient _client;

        public CmTestEnvironment(ISystemService system_service)
        {
            system_service.GetCredential(CM_API_TOKEN_ASSET_NAME, out SecureString api_token);
            var base_url = system_service.GetAsset(CM_API_BASE_URL_ASSET_NAME).ToString();

            this._project_name = system_service.GetAsset(CM_TEST_PROJECT_ASSET_NAME).ToString();
            this._client = new CmTestApiClient(new Uri(base_url), api_token);
            this._suppress_billing_confirmation = bool.Parse(
                system_service.GetAsset(CM_SUPPRESS_BILLING_CONFIRMATION_ASSET_NAME).ToString()
            );

            this._ct_source = new CancellationTokenSource(30000);
        }

        private void EnsureUserConsentsToAiUnitCharge()
        {
            if (!this._suppress_billing_confirmation)
            {
                string message =
                    "The operation you're about to perform will charge AI units, do you want to continue?";
                string caption = "Consent to AI unit Charge";
                MessageBoxButtons buttons = MessageBoxButtons.YesNo;
                DialogResult result;

                result = MessageBox.Show(message, caption, buttons);
                if (result != System.Windows.Forms.DialogResult.Yes)
                {
                    throw new Exception("User did not consent to AI unit charge");
                }
            }
            ;
        }

        public TestProject GetTestProject()
        {
            return new TestProject(this._project_name);
        }

        public async Task<TestDataset> CreateTestDataset(
            TestProject project,
            List<TestSource> sources
        )
        {
            string name = Guid.NewGuid().ToString();
            var request = new CreateDatasetRequest(
                new Dataset(sources.Select(source => source.Id).ToList())
            );
            await this._client.CreateDataset(project, name, request, this._ct_source.Token);
            return new TestDataset(project, name);
        }

        public async Task<TestSource> CreateTestSource(TestProject project)
        {
            String name = Guid.NewGuid().ToString();
            var request = new CreateSourceRequest(new NewSource());
            var response = await this._client.CreateSource(
                project,
                name,
                request,
                this._ct_source.Token
            );
            return new TestSource(project, name, response.Source.Id);
        }

        public async Task<TestStream> CreateTestStream(TestDataset dataset, NewStream stream)
        {
            var request = new CreateStreamRequest(stream);
            await this._client.CreateStream(dataset, request, this._ct_source.Token);

            return new TestStream(dataset, stream.Name, this._client);
        }

        public async Task<List<TestComment>> GenerateAndUploadTestComments(
            TestSource source,
            int number_of_comments
        )
        {
            EnsureUserConsentsToAiUnitCharge();
            List<TestComment> comments = new();
            for (int i = 0; i < number_of_comments; i++)
            {
                comments.Add(new TestComment());
            }
            await UploadTestComments(source, comments);

            return comments;
        }

        public async Task<SyncCommentsResponse> UploadTestComments(
            TestSource source,
            List<TestComment> test_comments
        )
        {
            List<Comment> comments = test_comments
                .Select(test_comment => test_comment.comment)
                .ToList();
            var request = new SyncCommentsRequest(comments);
            return await this._client.SyncComments(source, request, this._ct_source.Token);
        }

        public static Comment GenerateComment()
        {
            String random_string = Guid.NewGuid().ToString();
            Resources.Message message = new(random_string);

            return new Comment(
                random_string,
                DateTime.Now,
                new List<Resources.Message> { message }
            );
        }
    }

    public class TestComment
    {
        public Comment comment;

        public TestComment()
        {
            this.comment = CmTestEnvironment.GenerateComment();
        }

        public void SetUserProperty(String name, String value)
        {
            this.comment.UserProperties.Add($"string:{name}", value);
        }
    }

    public class TestProject
    {
        public string Name;

        public TestProject(string name)
        {
            this.Name = name;
        }
    }

    public class TestDataset
    {
        public string Name;
        public TestProject Project;

        public TestDataset(TestProject project, String name)
        {
            this.Project = project;
            this.Name = name;
        }
    }

    public class TestSource
    {
        public string Name;
        public TestProject Project;
        public string Id;

        public TestSource(TestProject project, String name, String id)
        {
            this.Project = project;
            this.Name = name;
            this.Id = id;
        }
    }

    public class TestCommentFilter
    {
        public CommentFilter CommentFilter { get; set; }

        public TestCommentFilter()
        {
            Dictionary<String, OneOfFilter> user_properties = new();
            this.CommentFilter = new CommentFilter(user_properties);
        }

        public void AddUserPropertyFilter(String propertyName, String value)
        {
            var one_of_filter = new OneOfFilter(){
                {"one_of", new List<String> { value }}
            };
            this.CommentFilter.UserProperties.Add($"string:{propertyName}", one_of_filter);
        }
    }

    public class TestStream
    {
        public String Name;
        public readonly TestDataset Dataset;
        private readonly CmTestApiClient _client;
        private readonly CancellationTokenSource _ct_source;

        public TestStream(TestDataset dataset, string name, CmTestApiClient client)
        {
            this.Name = name;
            this.Dataset = dataset;
            this._client = client;
            this._ct_source = new CancellationTokenSource();
        }

        public async Task<FetchStreamResponse> Fetch(int size)
        {
            var request = new FetchStreamRequest(size);
            return await this._client.FetchStream(this, request, this._ct_source.Token);
        }

        public async Task<bool> WaitForComments(int number_of_results, int filtered)
        {
            for (int i = 0; i < 60; i++)
            {
                var response = await this.Fetch(1024);

                if (response.Filtered == filtered && response.Results.Count == number_of_results)
                {
                    return true;
                }

                Thread.Sleep(2000);
            }
            return false;
        }
    }
}

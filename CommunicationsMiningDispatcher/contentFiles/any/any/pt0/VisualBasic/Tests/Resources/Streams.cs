using System;
using System.Collections.Generic;


namespace CommunicationsMiningDispatcher.Tests.Resources
{
    using OneOfFilter = Dictionary<String, List<String>>;


    public class CommentFilter
    {
        public Dictionary<String, OneOfFilter> UserProperties { get; set; }

        public CommentFilter(Dictionary<String, OneOfFilter> user_properties)
        {
            this.UserProperties = user_properties;
        }
    }

    public class CreateStreamRequest
    {
        public NewStream Stream { get; set; }

        public CreateStreamRequest(NewStream stream)
        {
            this.Stream = stream;
        }
    }

    public class NewStream
    {
        public CommentFilter CommentFilter { get; set; }
        public String Name { get; set; }

        public NewStream(CommentFilter comment_filter, String name)
        {
            this.CommentFilter = comment_filter;
            this.Name = name;
        }
    }

    public class CreateStreamResponse
    {
    }

    public class FetchStreamRequest
    {

        public int Size { get; set; }

        public FetchStreamRequest(int size)
        {

            this.Size = size;
        }
    }

    public class StreamResult
    {


    }

    public class FetchStreamResponse
    {
        public int Filtered { get; set; }
        public List<StreamResult> Results { get; set; }
    }

}

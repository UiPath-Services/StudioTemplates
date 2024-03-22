using System;
using System.Collections.Generic;

namespace CommunicationsMiningDispatcher.Tests.Resources
{
    public class SyncCommentsRequest
    {
        public List<Comment> Comments { get; set; }

        public SyncCommentsRequest(List<Comment> comments)
        {
            this.Comments = comments;
        }
    }

    public class SyncCommentsResponse { }

    public class Comment
    {
        public Comment(String id, DateTime timestamp, List<Message> messages)
        {
            this.Id = id;
            this.Timestamp = timestamp;
            this.Messages = messages;
            this.UserProperties = new Dictionary<String, String>();
        }

        public String Id { get; set; }
        public DateTime Timestamp { get; set; }
        public List<Message> Messages { get; set; }
        public Dictionary<String, String> UserProperties { get; set; }
    }

    public class Message
    {
        public Message(String body)
        {
            this.Body = new ContentPart(body);
        }

        public ContentPart Body { get; set; }
    }

    public class ContentPart
    {
        public ContentPart(String text)
        {
            this.Text = text;
        }

        public String Text { get; set; }
    }
}

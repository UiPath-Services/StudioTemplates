using System;


namespace CommunicationsMiningDispatcher.Tests.Resources
{
    public class CreateSourceRequest
    {
        public NewSource Source { get; set; }

        public CreateSourceRequest(NewSource source)
        {
            this.Source = source;
        }
    }

    public class CreateSourceResponse
    {
        public Source Source { get; set; }
    }

    public class NewSource { }

    public class Source
    {
        public String Id { get; set; }
    }
}

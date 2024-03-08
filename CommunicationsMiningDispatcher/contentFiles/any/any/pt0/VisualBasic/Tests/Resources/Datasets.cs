using System;
using System.Collections.Generic;


namespace CommunicationsMiningDispatcher.Tests.Resources
{
    public class CreateDatasetRequest
    {
        public Dataset Dataset { get; set; }

        public CreateDatasetRequest(Dataset dataset)
        {
            this.Dataset = dataset;
        }
    }

    public class CreateDatasetResponse { }

    public class Dataset
    {
        public Dataset(List<String> source_ids)
        {
            this.SourceIds = source_ids;
        }

        public List<String> SourceIds { get; set; }
    }
}

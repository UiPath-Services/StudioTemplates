using System;
using System.Collections.Generic;
using UiPath.Core;
using UiPath.Core.Activities;
using UiPath.Core.Activities.API;


namespace CommunicationsMiningDispatcher.Tests.Utils
{
    public class Orchestrator
    {

        private const string TEST_QUEUE_NAME = "InsertQueueNameHere";
        private const string TEST_FOLDER_NAME = "InsertFolderNameHere";
        private const int TIMEOUT_MS = 30000;

        public static IEnumerable<QueueItem> GetTestQueueItems(ISystemService system, DateTime from_time, int max)
        {
            var items = new List<QueueItem>();
            for (int i = 0; i < max; i += 100)
            {
                items.AddRange(system.GetQueueItems(TEST_QUEUE_NAME, TEST_FOLDER_NAME, null, from_time, null, QueueItemStates.All, null, new ReferenceFilterStrategy(), null, i, 100, TIMEOUT_MS));

            }

            return items;
        }
    }
}
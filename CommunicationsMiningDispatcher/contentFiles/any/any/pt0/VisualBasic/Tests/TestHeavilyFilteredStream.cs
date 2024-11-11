using System;
using System.Collections.Generic;
using System.Linq;
using CommunicationsMiningDispatcher.Tests.Resources;
using CommunicationsMiningDispatcher.Tests.Utils;
using UiPath.CodedWorkflows;


namespace CommunicationsMiningDispatcher.Tests
{
    public class TestHeavilyFilteredStream : CodedWorkflow
    {
        private const string TARGET_PROPERTY = "Target";
        private const string TARGET_VALUE = "FIND ME";
        private const string TEST_STREAM_NAME = "TEST";

        private List<TestComment> GetTargetComment()
        {
            var target_comment = new TestComment();
            target_comment.SetUserProperty(TARGET_PROPERTY, TARGET_VALUE);
            return new List<TestComment> { target_comment };
        }

        [TestCase]
        public void Execute()
        {
            Log("Test run started for TestHeavilyFilteredStream.");
            
            HashChecker.AssertGetDestinationQueueHasNotChanged();
            
            Log("Verifying Existing Queue State.");
            var test_start_time = DateTime.Now;
            var existing_queue_items = Orchestrator.GetTestQueueItems(system, test_start_time, 100);

            if (existing_queue_items.Count() != 0)
            {
                throw new Exception("Test Queue Not Empty");
            }
            
            Log("Setting Up CM Test Environment.");
            var test_environment = new CmTestEnvironment(system);
            var test_project = test_environment.GetTestProject();
            var test_source = test_environment.CreateTestSource(test_project).Result;
            var test_dataset = test_environment
                .CreateTestDataset(test_project, new List<TestSource> { test_source })
                .Result;
            var test_comment_filter = new TestCommentFilter();
            test_comment_filter.AddUserPropertyFilter(TARGET_PROPERTY, TARGET_VALUE);
            var new_stream = new NewStream(test_comment_filter.CommentFilter, TEST_STREAM_NAME);
            var test_stream = test_environment.CreateTestStream(test_dataset, new_stream).Result;

            Log("Uploading Test Comments to CM.");
            test_environment.GenerateAndUploadTestComments(test_source, 500).Wait();
            var target_comment = GetTargetComment();
            test_environment.UploadTestComments(test_source, target_comment).Wait();
            test_environment.GenerateAndUploadTestComments(test_source, 500).Wait();
            
            Log("Waiting for Test Stream to populate.");
            if (!test_stream.WaitForComments(1, 1000).Result)
            {
                throw new Exception("Commuications Mining Stream did not populate");
            }
            
            Log("Setting up test config file.");
            var init_setttings_result = RunWorkflow("Framework\\InitAllSettings.xaml", WorkflowUtils.GetInitSettingsInput());
            var config = WorkflowUtils.ReadConfigFromWorflowTask(init_setttings_result);

            config["CommunicationsMiningProjectName"] = test_project.Name;
            config["CommunicationsMiningDatasetName"] = test_dataset.Name;
            config["CommunicationsMiningStreamName"] = test_stream.Name;

            Log("Running Framework.");
            var main_inputs = WorkflowUtils.GetMainInput(config);
            RunWorkflow("Main.xaml", main_inputs);

            Log("Verifying Outputs.");
            var new_queue_items = Orchestrator.GetTestQueueItems(system, test_start_time, 100);

            if (new_queue_items.Count() != 1)
            {
                throw new Exception(String.Format("Expected 1 queue item but got {0}", new_queue_items.Count()));
            }

            var queue_item = new_queue_items.ElementAt(0);

            var communication_data = queue_item.SpecificContent.Get("CommunicationData").ToString();

            if (!communication_data.Contains(target_comment[0].comment.Id)){
                throw new Exception(String.Format("Created queue item does not contain target comment id"));
            }
            Log("Test Successful.");
        }
    }
}

using System;
using UiPath.CodedWorkflows;
using CommunicationsMiningDispatcher.Tests.Resources;


namespace CommunicationsMiningDispatcher.Tests
{
    public class TestGetDestinationQueueHasNotChanged : CodedWorkflow
    {
        [TestCase]
        public void Execute()
        {
            Log("Test run started for TestGetDestinationQueueHasNotChanged.");
            
            if (!HashChecker.HashMatches(HashChecker.GetDestinationQueuePath,HashChecker.ExpectedHashPath)){
                
                throw new Exception("GetDestinationQueue.xaml has changed. Please update or disable default tests.");
            }       
    
        }
    }
}
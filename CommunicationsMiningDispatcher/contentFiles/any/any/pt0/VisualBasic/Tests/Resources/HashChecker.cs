using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;

namespace CommunicationsMiningDispatcher.Tests.Resources
{
    public class HashChecker
    {

        public static String GetDestinationQueuePath = "Framework\\GetDestinationQueue.xaml";
        public static String ExpectedHashPath = "Tests\\Resources\\GetDestinationQueueExpectedHash.txt";


        public static bool HashMatches(String file_to_hash, String expected_hash_file)
        {
            var file_to_check_bytes = File.ReadAllBytes(file_to_hash);
            var expected_hash = File.ReadAllBytes(expected_hash_file);
            var hashed_file = SHA256.HashData(file_to_check_bytes);
            
            // You can use this to re-write the expected hash
            // File.WriteAllBytes(expected_hash_file, hashed_file);
            
            return hashed_file.SequenceEqual(expected_hash);
        }

        public static void AssertGetDestinationQueueHasNotChanged()
        {

            if (!HashMatches(GetDestinationQueuePath, ExpectedHashPath))
            {
                throw new Exception("GetDestinationQueue.xaml has changed. Please update or disable default tests.");
            }
        }

    }
}
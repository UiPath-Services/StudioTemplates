using System;
using System.Collections.Generic;

namespace CommunicationsMiningDispatcher.Tests.Utils
{
    public class WorkflowUtils
    {
        private const string CONFIG_FILE_PATH = "Data\\Config.xlsx";
        private static readonly string[] CONFIG_FILE_SHEETS = { "Settings", "Constants" };

        public static Dictionary<String, object> GetInitSettingsInput()
        {
            return new Dictionary<String, object> {
                {"in_ConfigFile", CONFIG_FILE_PATH},
                {"in_ConfigSheets", CONFIG_FILE_SHEETS},
            };
        }

        public static Dictionary<String, object> GetMainInput(Dictionary<String, object> config)
        {
            return new Dictionary<String, object> {
                {"in_Config", config}
            };
        }

        public static Dictionary<String, Object> ReadConfigFromWorflowTask(IDictionary<String, object> workflow_task)
        {
            return (Dictionary<String, object>)workflow_task.Get("out_Config");
        }
    }
}
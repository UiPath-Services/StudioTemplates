using System;
using System.Diagnostics;
using UiPath.CodedWorkflows;
using UiPath.Core;

namespace TestAutomationFramework.TestFramework.VideoRecording
{
    public class StopRecording : CodedWorkflow
    {
        [Workflow]
        public void Execute(Process in_ffmpegProcess, string in_VideoFilePath, bool in_startRecording)
        {
            Log("StopRecording - Start");

            if (in_startRecording)
            {
                try
                {
                    in_ffmpegProcess.StandardInput.WriteLine("q");
                    in_ffmpegProcess.StandardInput.Flush();
                    in_ffmpegProcess.WaitForExit();
                    Log("StopRecording - Recording has stopped");
                }
                catch (Exception ex)
                {
                    Log("StopRecording - Graceful stop failed, forcing kill: " + ex.Message, LogLevel.Warn);
                    in_ffmpegProcess.Kill();
                }
                finally
                {
                    testing.AttachDocument(in_VideoFilePath);
                    Log("StopRecording - Recording attached to test case");
                }
            }
            else
            {
                Log("StopRecording - Recording not started, skipping");
            }
        }
    }
}

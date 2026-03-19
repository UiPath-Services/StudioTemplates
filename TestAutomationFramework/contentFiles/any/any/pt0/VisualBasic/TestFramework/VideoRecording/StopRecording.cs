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
            Log("Stop recording process");

            if (in_startRecording)
            {
                try
                {
                    in_ffmpegProcess.StandardInput.WriteLine("q");
                    in_ffmpegProcess.StandardInput.Flush();
                    in_ffmpegProcess.WaitForExit();
                    Log("Recording has stopped");
                }
                catch (Exception)
                {
                    in_ffmpegProcess.Kill();
                }
                finally
                {
                    testing.AttachDocument(in_VideoFilePath);
                    Log("Recording attached to test case");
                }
            }
            else
            {
                Log("Recording not started. Skiping recording Stop");
            }
        }
    }
}

# Communications Mining Dispatcher Template Tests

To run these tests, you need to configure 4 Orchestrator assets (see
`TestEnvironment.cs`):
- _CmTestingApiToken_ - This is your Communications Mining Api Token (Text)
- _CmTestingBaseUrl_ - This is the base url of<F11>suppress your Communications
  Mining instance (Text)
- _CmTestingProjectName_ - This is the name of the project that the tests should
  be ran in (Text)
- _CmTestingSuppressBillingConfirmation_ - This is a value used to suppress the
  message box that asks the user to consent to the AI unit charge (Boolean)

Note: The project needs to already exist and the user that is running the tests needs all permissions


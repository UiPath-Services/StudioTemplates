### REFrameWork Template ###
**Robotic Enterprise Framework**

* Built on top of *Transactional Business Process* template
* Uses *State Machine* layout for the phases of automation project
* Offers high level logging, exception handling and recovery
* Keeps external settings in the *Data/Config.json* file; the transaction queue is selected on *Get Transaction Item* and recorded as a resource
* Pulls credentials from Orchestrator assets
* Gets transaction data from Orchestrator queue and updates back status
* Takes screenshots in case of system exceptions


### How It Works ###

1. **INITIALIZE PROCESS**
 + ./Framework/*InitAllSettings* - Load configuration data (settings and constants) from the Data/Config.json file
 + ./Framework/*InitiAllApplications* - Open and login to applications used throughout the process

2. **GET TRANSACTION DATA**
 + ./Framework/*GetTransactionData* - Fetches transactions from the Orchestrator queue selected on *Get Transaction Item* or any other configured data source

3. **PROCESS TRANSACTION**
 + *Process* - Process trasaction and invoke other workflows related to the process being automated 
 + ./Framework/*SetTransactionStatus* - Updates the status of the processed transaction (Orchestrator transactions by default): Success, Business Rule Exception or System Exception

4. **END PROCESS**
 + ./Framework/*CloseAllApplications* - Logs out and closes applications used throughout the process


### For New Project ###

1. Check the Data/Config.json file and add/customize any required settings and constants
2. Implement InitAllApplications.xaml and CloseAllApplications.xaml workflows, reading any values they need from the Config dictionary
3. Implement GetTransactionData.xaml and SetTransactionStatus.xaml according to the transaction type being used (Orchestrator queues by default)
4. Implement Process.xaml workflow and invoke other workflows related to the process being automated


### For Coding Agents ###

The guide for coding agents (Claude Code, Codex, Cursor and others) is `Framework/AGENTS.md`, with an
identical `Framework/CLAUDE.md`. It is kept there because Studio replaces the project-root
`AGENTS.md` and `CLAUDE.md` with its own generic files when it creates a project.

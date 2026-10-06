# CI Setup Documentation - Week 6

## 1. Objective
 To integrate Continuous Integration pipeline for Python secure project to automate build, security scan and test steps, simulating professional DevOps environment.

 ## 2. Project Setup
 I resued my Week 5 Security Enhancement project (Login + Notes App).Clean structure maintained: root has app files, tests/folser has pytest suite, .github/works/flows/ has ci.yml. Used requirements.txt for reproducible environment.

 ## 3. CI Tool Chosen
 GitHub Actions - chosen because it is free, widely used, integrates directly with GitHub repo, no extra server needed unlike Jenkins.

 ## 4. Pipeline Configuration Explained (ci.yml)
 on: push and pull_request to main/master -> triggers on every commit.

 jobs:
 - runs-on:ubuntu-latest
 -Steps:
  a) checkout@v4 - pulls code from repo 
  b) setup-python 3.10 - sets up Python environment
  c) pip install -r requirements.txt + pytest, bandit, bcrypt - installs dependencies
  d) Bandit scan - Scans app_secure.py  for high severity issues(-11). app_vulnerable.py is scanned  with || true so pipeline doesn't fail on known vulnerable file.
  e) pytest - Runs tests/test_secure.py with -v. Generates test_report.txt and cat shows logs in Actions.

  Pipeline is designed to FAIL if pytest fails or Bandit finds high severity in secure file, ensuring code quality gate.

  ## 5. Test Integration
  Created 4 automated tests in tests/test_secure.py: valid input, SQL injection block, DB creation. These tests validate the security fixes from Week 5. Every commit triggers these automatically.

  ## 6. Final Verification
  Made a small commit changing README.Went to Github Action tab - pipeline triggered  Automatically. All 4 tests passed. Logs show: 4 passed in 0.26s. Screenshot attached as Figure 1: Successful CI Run.

  ## 7 How to View Logs
  Github Repo -> Actions tab -> Click latest workflow run -> Click build-and-test job -> View step logs. Test report is visible via cat command in logs.

  ## 8. Conclusion
  CI pipeline successullly sutomates quality checks. It prevents vulnerable code from being merged, maintains high code quality through automation, exactly as expected in real-world professional environment. ZIP contains all files + screenshot  of CI run.
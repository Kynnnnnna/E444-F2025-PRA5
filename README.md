# E444-F2025-PRA5
This is an ECE444 lab that deploys machine learning models to the cloud using a cloud provider AWS Elastic Beanstalk.

## Screenshots
### Local Flask App Deployment
!['local deployment of flask app'](/screenshots/local_deployment.png)

### Elastic Beanstalk Deployment
!['eb deployment of flask app'](/screenshots/eb_deployment.png)

### Functional Test
#### Test Cases
| Test Case | Expected Result |
|-----------|-----------------|
|This is a real news. | "REAL" |
|This is a fake news. | "FAKE" |
|The government has announced a new policy to improve education. | "REAL" |
|Celebrity endorses miracle cure that doctors don't want you to know about! | "FAKE" |
#### Results
!['functional test results'](/screenshots/functional_test_results.png)

### Performance Test
!['performance test box plot'](/tests/latency_boxplot.png)
[100 runs for each test case results in excel sheet](/tests/performance_test_results.csv)
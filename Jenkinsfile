pipeline {
    agent any
    environment {
        SITENAME = 'your_sitename'
        ORG_ID = 'your_org_id'
        EMAIL = 'your_email'
        API_TOKEN = 'your_api_token'
    }
    stages {
        stage('Create Jira Team') {
            steps {
                script {
                    // Assuming your script is named create_team.py and is in the same directory
                    sh 'python3 create_team.py "$display_name"'
                }
            }
        }
    }
}

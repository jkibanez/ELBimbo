class awsEnvironment {
    String name
    String credentialsID

    // Constructor that properly initializes the class properties based on input parameters.
    awsEnvironment(Map params) {
        this.name = params.name
        this.credentialsID = params.credentialsID
    }
}


def awsEnvironments = [
    new awsEnvironment(
        name: "Avitru",
        credentialsID: 'infra-at-arcom'
    ),
    new awsEnvironment(
        name: "Flexplus",
        credentialsID: 'infra-at-flexplus'
    ),
    new awsEnvironment(
        name: "DCO Sandbox",
        credentialsID: 'infra-at-delsandbox'
    ),
    new awsEnvironment(    
        name: "DCO Secsandbox",
        credentialsID: 'infra-at-secsandbox'
    ),
    new awsEnvironment(    
        name: "Costpoint",
        credentialsID: 'infra-at-costpoint'
    ),
    new awsEnvironment(    
        name: "DCO",
        credentialsID: 'infra-at-dco'
    ),
    new awsEnvironment(    
        name: "Deltekdev",
        credentialsID: 'infra-at-dev'
    ),
    new awsEnvironment(    
        name: "DeltekEA",
        credentialsID: 'infra-at-deltekea'
    ),
    new awsEnvironment(    
        name: "EC-Maconomy-Sandbox",
        credentialsID: 'infra-at-ecmaconomy'
    ),
    new awsEnvironment(    
        name: "EC-MGT",
        credentialsID: 'infra-at-ec-mgt'
    ),
    new awsEnvironment(    
        name: "EC-SSEC",
        credentialsID: 'infra-at-ec-ssec'
    ),
    new awsEnvironment(    
        name: "Especs",
        credentialsID: 'infra-at-especs'
    ),
    new awsEnvironment(    
        name: "GlobalOSS",
        credentialsID: 'infra-at-oss'
    ),
    new awsEnvironment(    
        name: "GovWin",
        credentialsID: 'infra-at-govwinpd'
    ),
    new awsEnvironment(    
        name: "GovWinDev",
        credentialsID: 'infra-at-govwindv'
    ),
    new awsEnvironment(    
        name: "Interspec",
        credentialsID: 'infra-at-interspec'
    ),
    new awsEnvironment(    
        name: "Onvia, Inc.",
        credentialsID: 'infra-at-onvia'
    ),
    new awsEnvironment(    
        name: "Offsec",
        credentialsID: 'infra-at-offsec'
    ),
    new awsEnvironment(    
        name: "PieterEerlings",
        credentialsID: 'infra-at-pieter-eerlings'
    ),
    new awsEnvironment(    
        name: "ArchSandbox",
        credentialsID: 'infra-at-archsandbox'
    ),
    new awsEnvironment(    
        name: "SC-DHTMLX",
        credentialsID: 'infra-at-sc-dhtmlx'
    ),
    new awsEnvironment(    
        name: "SC-SSEC",
        credentialsID: 'infra-at-sc-ssec'
    ),
    new awsEnvironment(    
        name: "SC-Vantagepoint",
        credentialsID: 'infra-at-sc-vantagepoint'
    ),
    new awsEnvironment(    
        name: "ServiceBroker",
        credentialsID: 'infra-at-servicebroker'
    ),
    new awsEnvironment(    
        name: "Unionpoint",
        credentialsID: 'infra-at-unionpoint'
    ),
    new awsEnvironment(    
        name: "HRSmart",
        credentialsID: 'MarkSampayan_HRSmart'
    ),
    new awsEnvironment(    
        name: "ComputerEase",
        credentialsID: 'MarkSampayan_ComputerEase'
    )
]

pipeline {

    agent { label 'jenkins-slave-linux-cu01use1gs1jx01' }
    // agent any

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs( patterns: [[pattern: '*.csv', type: 'INCLUDE']])
            }
        }
        stage('Checkout Source') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: "*/main"]], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: "https://github.com/RodGuiamoy/AWS-Console-Login-Audit.git"]]])
            }
        }
        stage('Get IAM User Data') {
            steps {
                script {
                    awsEnvironments.each { environment ->
                        
                        credentialsID = environment.credentialsID
                        if (!credentialsID) {
                            unstable("Unable to find an AWS Credential for AWS environment ${environment.name}.")
                        }

                        def consoleAccessReport = []
                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',credentialsId: "${credentialsID}", accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                            try {
                                def cmd = "python3 get_console_access_report.py \"${environment.name}\""

                                consoleAccessReport = sh(script: cmd, returnStdout: true).trim()

                                // echo "IAM Users:\n${iamUsers}"
                                    
                            }
                            catch (Exception e) {
                                unstable("An error occurred:${e.message}")
                            }

                            if (consoleAccessReport.isEmpty()) {
                                unstable("No users returned.")
                            }
                        }
                    }
                }
            }
        }
        stage('Consolidate Data') {
            steps {
                script {

                    sh 'pip3 install pandas xlsxwriter'
                    sh 'pip3 install chardet'
                    
                    def cmd = "python3 consolidate_data.py"

                    sh(script: cmd, returnStdout: true).trim()
                }
            }
        }
        stage('Send Email') {
            steps {
                script {

                    def currentDate = new Date()
                    def formattedDate = currentDate.format("MMddyyyy")

                    emailext(
                        subject: "AWS Console Access Report - ${formattedDate}",
                        body: '',
                        mimeType: 'text/html',
                        from: 'CloudNoReply@deltek.com',
                        to: 'janrudolfguiamoy@deltek.com',
                        attachmentsPattern: "**/*${formattedDate}.xlsx" // Replace 'desired_file.txt' with your file name or pattern
                    )

                }
            }
        }
    }
}

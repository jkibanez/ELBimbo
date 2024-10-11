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
        name: "EC-MN-SB",
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
        credentialsID: 'infra-at-hrsmart'
    ),
    new awsEnvironment(    
        name: "ComputerEase",
        credentialsID: 'infra-at-computerease'
    )
]

pipeline {

    agent { label 'jenkins-slave-linux-cu01use1gs1jx01' }
    // agent any

    parameters {
        choice(
            name: 'AWSEnvironmentSelect',
            choices: ['ALL','ArchSandbox','Avitru','ComputerEase','CostPoint','DCO','DCO Sandbox','DCO Secsandbox','Deltekdev','DeltekEA','EC-MN-SB','EC-MGT','EC-SSEC','Especs','Flexplus','GlobalOSS','GovWin','GovWinDev','HRSmart','Interspec','Offsec','Onvia, Inc.','PieterEerlings','SC-DHTMLX','SC-SSEC','SC-Vantagepoint','ServiceBroker','Unionpoint']
            //choices: ['rod_aws']
        )
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs( patterns: [[pattern: '*.csv', type: 'INCLUDE']])
            }
        }
        stage('Checkout Source') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: "*/1-add-aws-environment-parameter"]], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: "https://github.com/jkibanez/ELBimbo.git"]]])
            }
        }
        stage('Get ELB Data') {
            steps {
                script {
                    
                    def selectedAWSEnvironments = []

                    if ( params.AWSEnvironmentSelect == 'ALL') {
                        selectedAWSEnvironments = awsEnvironments
                    }
                    else {
                        def selectedAWSEnvironment = awsEnvironments.find { it.name == params.AWSEnvironmentSelect }

                        if (selectedAWSEnvironment == null) {
                            error("Unable to find AWS environment ${params.AWSEnvironmentSelect} in AWS environments definition.")
                        }

                        selectedAWSEnvironments = [selectedAWSEnvironment]
                    }

                    // echo "${selectedAWSEnvironment.name}"

                    // def var1  = 'a'
                    // def var2 = ['a']

                    // for (i = 0; i < selectedAWSEnvironment.length; i++){
                    selectedAWSEnvironments.each { environment ->
                        // environment = selectedAWSEnvironment[i]

                        credentialsID = environment.credentialsID
                        if (!credentialsID) {
                            unstable("Unable to find an AWS Credential for AWS environment ${environment.name}.")
                        }

                        def albReport = []
                        def clbReport = []

                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',credentialsId: "${credentialsID}", accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                            try {
                                def cmd = "python3 alblist.py \"${environment.name}\""

                                albReport = sh(script: cmd, returnStdout: true).trim()

                                // echo "IAM Users:\n${iamUsers}"
                                    
                            }
                            catch (Exception e) {
                                unstable("An error occurred:${e.message}")
                            }

                            if (albReport.isEmpty()) {
                                unstable("Null return value.")
                            }

                            try {
                                def cmd = "python3 clblist.py \"${environment.name}\""

                                clbReport = sh(script: cmd, returnStdout: true).trim()

                                // echo "IAM Users:\n${iamUsers}"
                                    
                            }
                            catch (Exception e) {
                                unstable("An error occurred:${e.message}")
                            }

                            if (clbReport.isEmpty()) {
                                unstable("Null return value.")
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

                    // emailext(
                    //     subject: "AWS Load Balancer Report - ${formattedDate}",
                    //     body: '',
                    //     mimeType: 'text/html',
                    //     from: 'CloudNoReply@deltek.com',
                    //     to: 'CloudInfraSRE@deltek.com',
                    //     attachmentsPattern: "**/*${formattedDate}.xlsx" // Replace 'desired_file.txt' with your file name or pattern
                    // )

                    smtpServer = 'smtp.gss.mydeltek.local'
                    senderEmail = 'CloudNoReply@deltek.com'
                    recipientEmail = 'johnkennethibanez@deltek.com, janrudolfguiamoy@deltek.com'
                    subject = "AWS Load Balancer Report - ${formattedDate}"
                    body = ""
                    attachment = "AWS Load Balancer Report - ${formattedDate}.xlsx"
 
                    // Write the content to the file
                    // emailBodyFilePath = 'email_body.html'
                    // writeFile file: emailBodyFilePath, text: body
 
                    try {
 
                        def cmd = "python3 send_email.py \"${smtpServer}\" \"${senderEmail}\" \"${recipientEmail}\" \"${subject}\" \"\" \"${attachment}\""
 
                        scriptOutput = sh(script: cmd, returnStdout: true).trim()
                        echo "${scriptOutput}"
 
                        summary << new summaryItem(step: "SendEmail", result: "Success")
 
                    }
                    catch (Exception e) {
                        unstable("An error occurred:${e.message}")
                        summary << new summaryItem(step: "SendEmail", result: "Failed - ${e.message}")
                    }

                }
            }
        }
    }
}

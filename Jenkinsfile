podTemplate(
    idleMinutes : 10,
    podRetention : onFailure(),
    activeDeadlineSeconds : 3600,
    containers: [
        containerTemplate(
            name: 'dtk-rpm-builder', 
            image: 'docker-production.packages.idmod.org/idm/dtk-rpm-builder:0.1',
            command: 'sleep', 
            args: '30d'
            )
  ]) {
  properties([
            parameters([
                string(defaultValue: '-1', name: 'Version'),
                choice(choices: ['emod-generic', 'emod-hiv', 'emod-malaria', 'emod-tbhiv'], name: 'Package_Name')
        ])])
  node(POD_LABEL) {
    container('dtk-rpm-builder'){
		stage('Cleanup Workspace') {	    
			cleanWs()
			echo "Cleaned Up Workspace For Project"
		}
		stage("${params.Package_Name} ${params.Version}") {
			echo "Version is ${params.Version}."
			package_name = "${params.Package_Name}"
			echo "Package_Name is $package_name."
		}
		stage('Check out test script') {
			echo "Try to check out test scripts from YeChen-IDM/Jenkinsfile."
			git branch: "main",
			credentialsId: '704061ca-54ca-4aec-b5ce-ddc7e9eab0f2',
			url: 'git@github.com:InstituteforDiseaseModeling/Jenkinsfile.git'
		}
		stage('Check if version is in Staging') {
		    withCredentials([string(credentialsId: 'idm_bamboo_user', variable: 'user'), string(credentialsId: 'idm_bamboo_user_password', variable: 'password')]) {
					staging_version = sh(returnStdout: true, script: "pip3 index versions $package_name --index-url=https://$user:$password@packages.idmod.org/api/pypi/pypi-staging/simple").trim()
					println("$staging_version")
				}
			
			if ("${params.Version}" == "-1") {
			        staging_version = "$staging_version".split('\n')[0]
			        println("$staging_version")
			        version = sh(returnStdout: true, script: "echo '$staging_version' | cut -d '(' -f2 | cut -d ')' -f1").trim()
    		        println("Version is set to -1, reset it to the latest version: $version.")
    		    } else {
    		        if (staging_version.contains("${params.Version}")) {
                        println("Version ${params.Version} is found in staging.")
                        version = "${params.Version}"
                    } else {
                        println("Version ${params.Version} is not found in staging, please double check the version you entered.")
                        sh "exit 1"
                    }
    		    }
		}
		stage("Version is $version") {
		    echo "Version is $version"
		}
		stage('Pull from Staging') {
			echo "Trying to pull ${params.Package_Name} v$version from staging"
			def server = Artifactory.server 'jfrog-pypi-staging-deploy'
			def downloadSpec = """{
				 "files": [
				  {
					  "pattern": "idm-pypi-staging/$package_name/$version/",
					  "target": "staging/"
					}
				 ]
				}"""
			server.download spec: downloadSpec
			wheelFile = sh(returnStdout: true, script: "find staging/$package_name/$version -name '*.whl'").toString().trim()
			echo "This is the package file: ${wheelFile}"
		}
		stage('Sanity Check') {
			sh 'python3 --version'
			sh 'python3 -m pip install --upgrade pip'
			sh "pip3 install $wheelFile --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple"
			sh "pip3 freeze"
			sh "python3 scripts/test_${package_name}.py"
		}
		stage('Push to Production') {
			echo "Trying to push ${params.Package_Name} v$version to Production"
			def server_prod = Artifactory.server 'jfrog-pypi-prod-deploy'
			def uploadSpec = """{
			  "files": [
				{
				  "pattern": "staging/$package_name/$version/*",
				  "target": "idm-pypi-production/$package_name/$version/"
				}
			 ]
			}"""
			server_prod.upload spec: uploadSpec
		}
		stage('Sanity Check on Production package') {
		    sh "pip3 uninstall $package_name -y"
		    try {
    		    timeout(time: 3, unit: 'MINUTES') {
        		    waitUntil(initialRecurrencePeriod: 5000) {
                        script {
                            def prod_version = sh(returnStdout: true, script: "pip3 index versions $package_name --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple").trim()
                            if (prod_version.contains("$version")) {
                                println("v$version is there now!")
                                println("$prod_version")
                                return true
                            }else {
                                println("v$version is not there yet!")
                                println("$prod_version")
                                return false
                            }
                        }
                    }
    		    }
		    }
    		catch(err) {
            	println err
            	echo 'Time out reached.'
            	error "Failed to find version $version from pypi-production after 3 minutes."
    		}
			sh "pip3 install $package_name==$version --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple"
			sh "pip3 freeze"
			sh "python3 scripts/test_${package_name}.py"
		}
	}
 }
}

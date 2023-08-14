podTemplate(
    idleMinutes : 30,
    podRetention : onFailure(),
    activeDeadlineSeconds : 3600,
    containers: [
        containerTemplate(
            name: 'dtk-centos-buildenv', 
            image: 'testteam-docker-stage.packages.idmod.org/buildtest/idm/dtk-centos-buildenv:4.0',
            command: 'sleep', 
            args: '30d'
            )
  ]) {
  properties([
            parameters([
                gitParameter(branch: '',
                             branchFilter: 'origin/(.*)',
                             defaultValue: 'main',
                             description: '',
                             name: 'BRANCH',
                             quickFilterEnabled: false,
                             selectedValue: 'NONE',
                             sortMode: 'NONE',
                             tagFilter: '*',
                             type: 'PT_BRANCH')
        ])])
  node(POD_LABEL) {
    container('dtk-centos-buildenv'){
		stage('Cleanup Workspace') {	    
			cleanWs()
			echo "Cleaned Up Workspace For Project"
		}
		stage('Prepare') {
			sh 'python3 --version'
			sh 'pip3 --version'
			sh 'python3 -m pip install --upgrade pip'
			sh 'python3 -m pip install --upgrade setuptools'
			sh 'pip3 freeze'

			}
		stage('Code Checkout') {
			echo "I execute on the ${env.BRANCH} branch"
			git branch: "${env.BRANCH}",
			credentialsId: '704061ca-54ca-4aec-b5ce-ddc7e9eab0f2',
			url: 'git@github.com:jgsuresh/emod-genepi-archetypes.git'
		}
		stage('Install') {
			sh 'pip3 install -e . -r requirements.txt'
			sh 'pip3 freeze'
		}
		stage('Login to Comps') {
			withCredentials([string(credentialsId: 'Comps_emodpy_password', variable: 'password')]) {
					sh 'python3 "workflow/create_auth_token_args.py" --comps_url https://comps.idmod.org --username yechen --password $password'
				}
		}
		stage('Get Binary') {
			dir('get_latest_binary') {
				sh 'python3 get_latest_binary.py'
			}
		}
		stage('Run Tests') {
			dir('test') {
				sh "pip3 install pytest pytest-xdist pytest-order"
				sh 'pytest -n 10 --dist loadfile -vv --junitxml="result.xml"'
				junit '*.xml'
			}
		}
 	}
 }
}

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
    container('dtk-rpm-builder'){
		stage('Cleanup Workspace') {	    
			cleanWs()
			echo "Cleaned Up Workspace For Project"
		}
	}
 }
}

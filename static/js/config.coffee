require.config
    baseUrl: '/static/js'
    paths: 
        'jQuery': '//dn-staticfile.qbox.me/jquery/2.0.3/jquery.min'
        'bootstrap': '//catke-static.b0.upaiyun.com/bootstrap/3.0.0/bootstrap.min'
        'angular': '//dn-staticfile.qbox.me/angular.js/1.1.5/angular.min'
        'angular-resource': '//dn-staticfile.qbox.me/angular.js/1.1.5/angular-resource.min'
    shim:
        'angular' : {'exports' : 'angular'}
        'angular-resource': { deps:['angular']}
        'jQuery': {'exports' : 'jQuery'} 
        'bootstrap': { deps:['jQuery']}
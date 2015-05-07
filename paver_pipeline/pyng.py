from execjs import get
import sys
import os.path as op

rt = get('Node')

context = rt.compile('''        
module.paths.push('%s');
function seePath(){
    return module.paths;
}
var ng = require('ng-annotate');
function annotate(src,cfg){
    return ng(src,cfg);
}''' % op.realpath(
                op.join(
                     op.dirname(
                         op.dirname(
                              __file__
                            
                         )),'node_modules'
                 )
         )
)

def ng_annotate(src,cfg=None):
    return context.call('annotate',src,cfg or dict(add=True)).get('src',None)


coffee = '''
var app = angular.module('my.app',[]);

app.controller('TestCtrl',function($scope){
    
});
'''

def test():
    #print ng_annotate(coffee)

    print context.call('seePath')


def main():
    print ng_annotate(open(sys.argv[-1],'r').read(),'')

if __name__ == "__main__":
    #main()
    test()
    #op.realpath(op.join(op.dirname(op.dirname( __file__)),'node_modules'))


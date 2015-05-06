from execjs import get
import sys
import os.path as op

rt = get('Node')

context = rt.compile('''        
module.paths.push('%s');
var ng = require('ng-annotate');
function annotate(src,cfg){
    return ng(src,cfg);
}''' % op.join(
            op.dirname(
                    __file__
            ),'node_modules'
      )
)

def ng_annotate(src,cfg=None):
    return context.call('annotate',src,cfg or dict(add=True))['src']


coffee = '''
var app = angular.module('my.app',[]);

app.controller('TestCtrl',function($scope){
    
});
'''

def test():
    print ng_annotate(coffee)


def main():
    print ng_annotate(open(sys.argv[-1],'r').read())

if __name__ == "__main__":
    main()

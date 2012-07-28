# -*- coding: utf-8 -*-

import sys
import os
import commands
from kay.management.utils import (
    print_status, create_db_manage_script
    )
DUMP = 1
RESTORE = 2

def js_compile():
    args = []
    args.extend(sys.argv[2:])
    os.system('java -jar media/SoyToJsSrcCompiler.jar --shouldProvideRequireSoyNamespaces --cssHandlingScheme GOOG --outputPathFormat media/js/template.soy.js media/soy/tsuhan.soy')
    os.system('java -jar media/closure-stylesheets.jar --output-file media/css/tsuhan_style.css --output-renaming-map media/js/renaming_map.json --output-renaming-map-format JSON --rename CLOSURE media/gss/*.gss media/gss/closure/*.css')
    os.system('java -jar media/closure-stylesheets.jar --output-file media/css/tsuhan_style.css --output-renaming-map media/js/renaming_map.js --output-renaming-map-format CLOSURE_COMPILED --rename CLOSURE media/gss/*.gss media/gss/closure/*.css')
    os.system('python ../closure-library/closure/bin/build/closurebuilder.py --root=../closure-library --root=media -n tsuhan.App -o compiled --output_file=media/js/tsuhan_compile.js -c media/compiler.jar -f "--compilation_level=ADVANCED_OPTIMIZATIONS" -f "--js=media/js/renaming_map.js" -f "--define=goog.DEBUG=false"')
    os.system('python manage.py compile_media')
    print_status('')

js_compile.passthru = True
action_js_compile = js_compile
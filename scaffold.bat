@echo off

:: Create main project directory
mkdir project_root
cd project_root

:: Create infrastructure directories
mkdir infrastructure\cdk\stacks
mkdir infrastructure\scripts

:: Create backend directories
mkdir backend\src\handlers
mkdir backend\src\models
mkdir backend\src\services
mkdir backend\src\utils
mkdir backend\tests\unit
mkdir backend\tests\integration

:: Create frontend directories
mkdir frontend\public
mkdir frontend\src\components
mkdir frontend\src\pages
mkdir frontend\src\services
mkdir frontend\src\styles

:: Create empty files
type nul > infrastructure\cdk\app.py
type nul > infrastructure\cdk\stacks\backend_stack.py
type nul > infrastructure\cdk\stacks\frontend_stack.py
type nul > infrastructure\cdk\stacks\networking_stack.py
type nul > infrastructure\cdk\requirements.txt
type nul > infrastructure\scripts\deploy.bat
type nul > infrastructure\scripts\destroy.bat

type nul > backend\src\handlers\__init__.py
type nul > backend\src\handlers\user_handler.py
type nul > backend\src\handlers\product_handler.py
type nul > backend\src\models\__init__.py
type nul > backend\src\models\user.py
type nul > backend\src\models\product.py
type nul > backend\src\services\__init__.py
type nul > backend\src\services\user_service.py
type nul > backend\src\services\product_service.py
type nul > backend\src\utils\__init__.py
type nul > backend\src\utils\helpers.py
type nul > backend\requirements.txt
type nul > backend\README.md

type nul > frontend\public\index.html
type nul > frontend\public\favicon.ico
type nul > frontend\src\App.js
type nul > frontend\src\index.js
type nul > frontend\package.json
type nul > frontend\README.md
type nul > frontend\.gitignore

type nul > .gitignore
type nul > README.md
type nul > requirements.txt

echo Project structure created successfully!

1. Установка wsl: wsl --install -d Ubuntu-22.04
2. Проверка установки: wsl -l
3. Установка mc:
	- sudo apt update																# Обновить
	- sudo apt install mc															# Установить mc
4. Установка ArduPilot:
	- cd																			# Переходим в кореневую папку	
	- sudo git clone --recursive https://github.com/KruglovDmitry/ardupilot.git 	# Клон моего featch репозитория ArduPilot
	- sudo chown -R <user> /home/dima/ardupilot										# Устанавливаем контроль папки репозитория
	- cd ardupilot																	# В репозиторий	
	- Tools/environment_install/install-prereqs-ubuntu.sh -y						# Установка зависимостей
	- . ~/.profile																	# Перезагрузка окружения (deactivate - выйти)
	- ./waf configure --board MambaF405v2											# Конфигурируем под полетный контроллер mamba
	- ./waf copter																	# Запускаем сборку контроллера (./waf clean - очистить)
	- code .																		# Открываем в VS code
	- cd ~/ardupilot/ArduCopter														# В папку ArduCopter
	- ../Tools/autotest/sim_vehicle.py --map --console								# Запуск тестовой симуляции
5. Установка VcXsrv:
	- https://sourceforge.net/projects/vcxsrv/										# Скачиваем и устанавливаем
	- Запустить -> Set multi display -> Allow agreement								# Настраиваем дисплеи и разрещения
	- export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}'):0	# Устанавливаем переменную (localhost:0)
6. Установка PX4 (включая jmavsim):
	- cd																			# Переходим в кореневую папку
	- sudo apt update && sudo apt upgrade -y										# Обновляем
	- sudo apt install ant															# Устанавливаем сборщик ant
	- sudo apt install openjdk-11-jdk												# Установть Java 11 sdk
	- sudo update-alternatives --config java										# Если нужна другая версия Java
	- sudo git clone https://github.com/PX4/PX4-Autopilot.git --recursive			# Клонируем репозиторий PX4
	- sudo chown -R <user> /home/dima/PX4-Autopilot									# Устанавливаем контроль папки репозитория
	- cd ~/PX4-Autopilot															# В папку PX4-Autopilot
	- bash ./Tools/setup/ubuntu.sh													# Запуск скрипта сборки
	- make px4_sitl jmavsim															# Запуск
7. Установка jmavsim (отдельно от PX4):
	- cd																			# Переходим в кореневую папку
	- sudo apt update && sudo apt upgrade -y										# Обновляем
	- sudo apt install ant															# Устанавливаем сборщик ant
	- sudo apt install openjdk-11-jdk												# Установть Java 11 sdk
	- sudo apt-get install libvecmath-java											# Установить libvecmath-java
	- sudo git clone https://github.com/PX4/jMAVSim.git								# Клонируем репозиторий jmavsim
	- sudo chown -R <user> /home/dima/jMAVSim										# Устанавливаем контроль папки репозитория
	- cd ~/jMAVSim																	# В репозиторий
	- sudo git submodule init														# Регистрируем модули
	- sudo git submodule update														# Обновляем модули
	- sudo ant create_run_jar copy_res												# Собираем
	- cd out/production																# В папку cd out/production
	- java -Djava.ext.dirs= -jar jmavsim_run.jar 									# Запуск
6. Установка gazebo:
	- cd																			# Переходим в кореневую папку
	- sudo apt update																# Обновляем
	- sudo apt install gazebo														# Устанавливаем gazebo
	- sudo apt install libgz-sim8-dev rapidjson-dev									# Устанавливаем зависимости для Harmonic
	- sudo apt install libopencv-dev libgstreamer1.0-dev 
		/ libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad 
		/ gstreamer1.0-libav gstreamer1.0-gl
	- sudo git clone https://github.com/ArduPilot/ardupilot_gazebo					# Клонируем репозиторий ardupilot_gazebo
	- sudo chown -R <user> /home/dima/ardupilot_gazebo								# Устанавливаем контроль папки репозитория
	- cd ardupilot_gazebo															# В репозиторий
	- mkdir build && cd build														# Создаем папку для сборки
	- cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo									# Готовим сборку
	- make -j4																		# Собираем	
	- export GZ_SIM_SYSTEM_PLUGIN_PATH=												# Добавляем переменные среды
					$HOME/ardupilot_gazebo/build:$GZ_SIM_SYSTEM_PLUGIN_PATH
	- export GZ_SIM_RESOURCE_PATH=
					$HOME/ardupilot_gazebo/models:$HOME/ardupilot_gazebo/worlds:$GZ_SIM_RESOURCE_PATH
	- gz sim -v4 -r iris_runway.sdf													# Тестовый запуск
7. Запуск симуляции gazebo:
	- cd /home/dima/ardupilot														# Переходим в папку репозитория ardupilot
	- code .																		# Запускаем VS Code 
	- cd /home/dima/ardupilot_gazebo												# Переходим в папку репозитория gazebo
	- gz sim -v4 -r iris_runway.sdf													# Запускаем симуляцию gazebo (проверить переменные среды)
	- cd /home/dima/ardupilot														# Переходим в папку репозитория ardupilot (новый терминал)
	- sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console		# Запускаем симулятор с внешним портом
		/ --out=udp:127.0.0.1:14551													# (проверяем что в строке подключения указан порт 14551)
	- python <filename>.py															# Запускаем в другом терминале VS скрипт с кодом
8. Запуск симуляции с jmavsim:
	- cd /home/dima/ardupilot														# Переходим в папку репозитория ardupilot
	- code .																		# Запускаем VS Code
	- cd /home/dima/jMAVSim/out/production											# Переходим в папку репозитория jMAVSim/out/production
	- java -jar jmavsim_run.jar														# Запускаем симуляцию jmavsim
	- cd /home/dima/ardupilot														# Переходим в папку репозитория ardupilot (новый терминал)
	- sim_vehicle.py -v ArduCopter -f quad --console --map							# Запускаем симулятор с внешними портами
		/ --out=udp:127.0.0.1:14551													# (проверяем что в строке подключения указан порт 14551)
		/ --out=udp:0.0.0.0:14560													# (порт jmavsim)
	- python <filename>.py															# Запускаем в другом терминале VS скрипт с кодом
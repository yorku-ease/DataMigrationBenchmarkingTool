version: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporter
      version: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporterversion: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporterversion: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporterversion: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporterversion: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporterversion: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporterversion: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporterversion: '3'
services:
  node-exporter:
    network_mode: "host"
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - 9100:9100
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 9100 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    network_mode: "host"
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - "/dev/disk/:/dev/disk"
    privileged: true
    devices: 
      - "/dev/kmsg"
  controller:
    image: fareshamouda/controller:latest
    privileged: true
    container_name: controller
    environment:
      - FOLDERS_PATH=$PWD
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - cadvisor
      - node-exporter
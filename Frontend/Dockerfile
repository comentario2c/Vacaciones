# Usamos Node.js
FROM node:20

# Carpeta de trabajo
WORKDIR /app

# Copiamos el código Angular
COPY . .

# Instalamos dependencias
RUN npm install

# Exponemos el puerto 4200
EXPOSE 4200

# Comando por defecto
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0"]
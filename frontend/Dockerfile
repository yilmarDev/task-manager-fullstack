FROM node:20-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias
COPY package.json package-lock.json* ./

# Instalar las dependencias de npm
RUN npm install

# Copiar el resto de los archivos del frontend
COPY . .

# Exponer el puerto por defecto de Vite
EXPOSE 5173

# Levantar el entorno de desarrollo y exponer al host
CMD ["npm", "run", "dev", "--", "--host"]

# Используем официальный Nginx образ
FROM nginx:1.25-alpine

# Удаляем дефолтную конфигурацию
RUN rm /etc/nginx/conf.d/default.conf

# Копируем нашу конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf

# Создаем директории для статики
RUN mkdir -p /usr/share/nginx/html/static /usr/share/nginx/html/media

# Устанавливаем корректные права
RUN chown -R nginx:nginx /usr/share/nginx/html

# Открываем порты
EXPOSE 80 443

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]
FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    libpq-dev \
    git \
    curl \
    libzip-dev \
    unzip \
    npm \
    && apt-get clean

RUN docker-php-ext-install pdo pdo_pgsql zip bcmath

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html
COPY . .

RUN composer install --no-interaction --no-scripts --optimize-autoloader

RUN composer run-script post-autoload-dump

RUN npm install && npm run build
RUN chmod -R 775 storage bootstrap/cache

EXPOSE 8000
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
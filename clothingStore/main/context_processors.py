def user_context(request):
    return {
        'is_authenticated': 'user_id' in request.session,
        'is_superuser': request.session.get('is_superuser', False),  # Добавляем проверку на superuser
    }

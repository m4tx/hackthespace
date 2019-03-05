from django.contrib import admin

from game.models import Player, SolvedPuzzle


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'email', 'last_puzzle')
    search_fields = ('session_id', 'email')
    readonly_fields = ('last_puzzle',)


@admin.register(SolvedPuzzle)
class SolvedPuzzleAdmin(admin.ModelAdmin):
    list_display = ('player', 'puzzle', 'timestamp')
    list_filter = ('puzzle',)
    search_fields = ('player__session_id', 'player__email', 'puzzle')

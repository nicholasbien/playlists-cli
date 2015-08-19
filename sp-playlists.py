import sys
import threading
import spotify

def create_artist_recommendations_playlist(session, artist_query):
    print('Searching for artist')
    search = session.search(artist_query)
    search.load()
    artist = search.artists[0]
    artist_name = artist.name
    browser = artist.browse()
    browser.load()

    tracks = []
    print('Finding similar artists')
    for similar_artist in browser.similar_artists:
        browser = similar_artist.browse()
        browser.load()
        if len(browser.tophit_tracks) > 1:
            top_track = browser.tophit_tracks[0]
            tracks.append(top_track)

    print('Loading new playlist')
    container = session.playlist_container
    playlist = container.add_new_playlist('Recommendations: ' + artist_name, 0)
    playlist.add_tracks(tracks)
    playlist.load()

def main():
    if len(sys.argv) < 4:
        print('Input form: [username] [password] "[artist]"')
        exit()

    print('Logging in to Spotify')
    logged_in_event = threading.Event()
    def connection_state_listener(session):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            logged_in_event.set()

    session = spotify.Session()
    loop = spotify.EventLoop(session)
    loop.start()
    session.on(
        spotify.SessionEvent.CONNECTION_STATE_UPDATED,
        connection_state_listener)

    session.login(sys.argv[1], sys.argv[2])
    logged_in_event.wait()

    create_artist_recommendations_playlist(session, sys.argv[3])

if __name__ == '__main__':
    main()
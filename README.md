### command-line client for mastodon

Want to enjoy Mastodon while working? We can help.

### Setup

```zsh
$ pip3 install git+https://github.com/huyfififi/tusk.git@main 
$ export MASTODON_INSTANCE_DOMAIN={YOUR_INSTANCE_DOMAIN}  # e.g., mastodon.social
$ # access token can be obtained Preference -> Deployment -> New application
$ export MASTODON_ACCESS_TOKEN={YOUR_ACCESS_TOKEN}
```

### Usage

```zsh
$ tusk timeline
110830292655627088
xxxxx
foo

110830327447208246
xx
Someone on here is possessed by an owl.

110830417021502265
xxxxxxxx
This is a test post

$ tusk notifications
xx
favourite
xxxxxxxxxx
x...xxxxx...

xxxxxxxx
follow

xxx
favourite
xxxxxxxxxx
xxxxxxxxxxxxxxxx...xxx....

$ tusk post 555 456 0721
Successfully posted a status.
110830543741158158
Xxxxxxxxx
555 456 0721

$ tusk favorite 110830543741158158
Successfully favourited the status.
110830543741158158
Xxxxxxxxxx
555 456 0721

$ tusk delete 110830543741158158
Successfully deleted the status.
110830543741158158
Xxxxxxxxxx
555 456 0721

$ tusk whoami
{'acct': 'xxxxxxxxxxx',
 'avatar': 'https://s3-us-east-2.amazonaws.com/.../bef2ec6b0f65629e.png',
 'avatar_static': 'https://s3-us-east-2.amazonaws.com/.../bef2ec6b0f65629e.png',
 'bot': False,
 'created_at': '2022-12-27T00:00:00.000Z',
 'discoverable': True,
 'display_name': 'xxxxxxxxxx',
 'emojis': [],
 'fields': [],
 'followers_count': 24,
 'following_count': 32,
 'group': False,
 'header': 'https://s3-us-east-2.amazonaws.com/.../196358ca60a94001.png',
 'header_static': 'https://s3-us-east-2.amazonaws.com/.../196358ca60a94001.png',
 'id': '109588273352064062',
 'last_status_at': '2023-08-04',
 'locked': False,
 'noindex': False,
 'note': '<p>xxxxxxxxxx</p>',
 'role': {'color': '',
          'highlighted': True,
          'id': '3',
          'name': 'Owner',
          'permissions': '1048575'},
 'source': {'fields': [],
            'follow_requests_count': 0,
            'language': None,
            'note': 'xxxxxxxxxx',
            'privacy': 'public',
            'sensitive': False},
 'statuses_count': 2123,
 'url': 'https://foo.com',
 'username': 'xxxxxxxxx'}

$ tusk following
{'acct': 'bar@bar.com',
 'display_name': 'xx',
 'id': '109588442526443837',
 'note': 'XxxXxxxxxXXX\n'
         'XXXxX\n'
         '\n'}
{'acct': 'foo@foo.com',
 'display_name': 'xxxxx',
 'id': '109588425349181950',
 'note': 'xxxxxXxx..xXxXxxX'
         'XxXxxxxxxxXxxxx...xxxXXXXxXxXXXxxxX\n'
         '\n'}

$ tusk followers
{'acct': 'bar@bar.com',
 'display_name': 'xx',
 'id': '109588442526443837',
 'note': 'XxxXxxxxxXXX\n'
         'XXXxX\n'
         '\n'}
{'acct': 'foo@foo.com',
 'display_name': 'xxxxx',
 'id': '109588425349181950',
 'note': 'xxxxxXxx..xXxXxxX'
         'XxXxxxxxxxXxxxx...xxxXXXXxXxXXXxxxX\n'
         '\n'}

$ tusk block --list
{'acct': 'bar@bar.social',
 'display_name': 'xxxxx',
 'note': 'Xxx xxxx xxxx xxx xxxxxxxx.\n'
         '\n'}
{'acct': 'foo@foo.social',
 'display_name': 'Xxxxxxx Xxxxxx',
 'note': 'Xxxxx xxxxxx, xxxxxxx, xxx xxxxxxx'
         'Xxxxxxx X'x\n'
         'xx xxxxx xxxxxx xxxx.\n'
         '\n'}
```

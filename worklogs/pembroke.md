
### 2021-11-19 00:11:49.294572: clock-in

### 2021-11-19 05:03:37.848482: clock-out

* bugfix
* filtered by user
* led display

### 2021-11-18 23:41:39.328501: clock-in: T-1h30m 

### 2021-11-18 22:41:18.721288: clock-out

* disabled status

### 2021-11-18 22:12:44.331662: clock-in

### 2021-11-18 20:10:50.272435: clock-out


### 2021-11-18 19:44:30.848769: clock-in

### 2021-11-18 19:33:39.227201: clock-out


### 2021-11-18 19:22:18.461858: clock-in

### 2021-11-18 13:57:58.467129: clock-out

* logo from url, qr popover, cosmetics

### 2021-11-18 11:43:38.414271: clock-in

### 2021-11-18 11:24:39.671634: clock-out: T-5m 

* need to rebuild container to grab dash-boostrap-components==1.0.0

### 2021-11-18 14:55:40.352875: clock-in

### 2021-11-17 19:16:38.510411: clock-out

* need to communicate invoice details as a message. can store as json with memo

Generate a private key for use with hourly

```sh
ssh-keygen -t ed25519 -C "your_email@example.com"
# follow prompts and save as path/to/hourly_id_ed25519
# this will automatically generate path/to/hourly_id_ed25519.pub
```

Interesting, `ed25519` isn't used for encryption, only signing https://blog.filippo.io/using-ed25519-keys-for-encryption/

fernet actually has symmetric encryption https://cryptography.io/en/latest/fernet/#fernet-symmetric-encryption

but we need asymmetric encryption https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/

> If you want to encrypt large blocks asymmetrically, the usual solution is a hybrid construction: randomly generate a symmetric key, encrypt and authenticate your data with that, and then encrypt that key with the RSA key. https://github.com/pyca/cryptography/issues/5685

### 2021-11-17 16:43:49.407959: clock-in

### 2021-11-16 11:53:59.963286: clock-out

Todo for demo:

1. display price in dollars
1. create, commit invoice from worker side
1. execute invoice on payer side

### 2021-11-16 09:45:38.756935: clock-in

### 2021-11-14 10:10:25.648694: clock-out

* ssh keys with gitpython https://medium.com/@tzuni_eh/git-commit-with-gitpython-and-ssh-key-926cad91ca89
* ssh key provisioning with gitpython https://stackoverflow.com/questions/28291909/gitpython-and-ssh-keys

### 2021-11-14 10:06:22.886468: clock-in: T-5m 

### 2021-11-13 12:28:53.862680: clock-out

* qr code generation

### 2021-11-13 16:17:39.066115: clock-in

### 2021-11-13 15:56:27.050541: clock-out


### 2021-11-13 09:58:24.901493: clock-in

### 2021-11-12 17:17:54.820363: clock-out: T-20m 


### 2021-11-12 16:07:15.650174: clock-in

### 2021-11-12 12:24:05.461855: clock-out: T-10m 

* merging bugfix from master


### 2021-11-12 10:13:36.666930: clock-in

* hackathon conf
### 2021-11-05 21:05:38.628081: clock-out


### 2021-11-05 21:04:59.226235: clock-in

### 2021-11-05 21:04:40.273819: clock-out

* invoice generation proof of concept
* added lightning grpc
* running hourly in plebenet playground
* generated test invoice

### 2021-11-05 11:35:40.005987: clock-in: T-30m 

### 2021-11-04 22:56:04.342366: clock-out

* tried to get docker container running on windows, but ran into mounting issues
* got dashboard to run on windows
* needed to set GIT_USER_NAME to match exactly with previous clock in commit

### 2021-11-05 01:38:32.783763: clock-in

### 2021-11-05 01:35:04.019470: clock-out


### 2021-11-04 20:08:51.896212: clock-in

### 2021-10-19 04:03:29.521261: clock-out

* sorting by time
* fixed button children, buttons working

### 2021-10-19 03:24:24.827527: clock-in

### 2021-10-19 03:24:16.778547: clock-out

* clicking clock out button should changed "clocked in" button to "clock in"

### 2021-10-19 03:19:01.435458: clock-in

### 2021-10-19 03:18:53.143795: clock-out


### 2021-10-19 03:16:26.428876: clock-in

### 2021-10-19 03:16:05.150957: clock-out


### 2021-10-19 03:07:01.424080: clock-in

### 2021-10-19 02:15:19.311658: clock-out


### 2021-10-18 21:00:00.665679: clock-in

### 2021-10-17 23:24:57.991280: clock-out

* commit author
* added tabs, commit author

### 2021-10-18 04:21:49.851718: clock-in

### 2021-10-18 04:20:26.553289: clock-out

### 2021-10-18 03:57:38.837050: clock-out


### 2021-10-17 22:07:11.281903: clock-in

### 2021-10-17 16:25:23.021970: clock-out


### 2021-10-17 15:37:55.248115: clock-in

### 2021-09-30 21:18:36.224621: clock-out

* adding inout to dashboard
* `process_commit` needs to use registered id

### 2021-09-30 19:26:53.261218: clock-in

### 2021-09-30 00:04:21.838617: clock-out

* separate in/out buttons

### 2021-09-29 23:22:58.657224: clock-in

### 2021-09-28 23:57:52.543075: clock-out

* trying toggle switch

### 2021-09-28 23:25:14.324913: clock-in

### 2021-09-27 23:18:48.655650: clock-out

* basic layout, clock in/out counter

### 2021-09-27 21:31:42.053205: clock-in

### 2021-09-27 21:09:01.740071: clock-out


### 2021-09-27 21:03:33.790613: clock-in

### 2021-09-26 22:33:15.023326: clock-out

* version push

### 2021-09-26 22:32:43.479051: clock-in: T-30m 

### 2021-09-26 13:48:59.580563: clock-out

* merging multi-repo-conf
* merging multi-repo-conf
* fixed timedelta bug
* BUG fixed required clock statement
* BUG fixed time shift update
* moving into worklogs
* saw this when clocking in

`rosetta error: ThreadContext::resume failed 4`

### 2021-09-26 13:13:08.492389: clock-in

### 2021-07-23 01:06:09.646169: clock-out

* fixed time adjustment with message bug

### 2021-07-22 22:52:16.602663: clock-in

* removing requirements file
### 2021-05-15 16:17:11.997280: clock-out

* added bugfix for multi named repos

### 2021-05-15 16:16:43.647226: clock-in

### 2021-05-15 16:07:06.595128: clock-out: T-20m 

* bug preventing multiple names from adding across multiple repos

### 2021-05-15 15:15:48.282768: clock-in

### 2021-04-06 00:20:14.862558: clock-out

* added division of labor for multiple repo names

### 2021-04-05 22:00:06.101441: clock-in

### 2020-08-07 11:57:14.484755: clock-out

* added normalization without second axis

### 2020-08-07 11:32:29.729332: clock-in

### 2020-07-29 20:42:30.976371: clock-out

* added average time

### 2020-07-29 19:09:05.013725: clock-in: T-30m 

### 2020-07-29 17:32:59.062285: clock-out


### 2020-07-29 17:03:52.631490: clock-in

* fixed tz localize error
* fixed timedelta update again
* fixing time adjustment
### 2020-04-05 23:12:17.506294: clock-out

* got groupings to work by name or repo

### 2020-04-05 23:10:16.904078: clock-in: T-30m 

### 2020-04-05 22:33:49.515939: clock-out: T-5h 


### 2020-04-05 17:27:29.678827: clock-in

### 2020-04-05 13:51:53.130898: clock-out

* bug fixes

### 2020-04-05 13:36:21.847920: clock-in

### 2020-04-05 13:18:53.515173: clock-out

* fixing bugs not allowing group by name

### 2020-04-05 12:06:16.000383: clock-in

### 2020-04-05 11:05:49.617937: clock-out

* grouping by name

### 2020-04-05 11:00:51.458868: clock-in

* updating multi repo docs
### 2020-04-05 00:22:24.450956: clock-out: T-10m 

* adding multi repo docs

### 2020-04-04 23:20:09.144648: clock-in

### 2020-04-04 15:12:34.630127: clock-out

* added 'report.grouping' to specify name, email, repo, branch
* got multiple branches to work
* moved cli arg override into config_override
* fixed bug preventing command line args from overriding those specified in config_override

### 2020-04-04 12:38:56.777222: clock-in

### 2020-04-01 16:50:06.390562: clock-out

* set default repo name to empty str (pandas groupby ignores `None` values)

### 2020-04-01 16:32:39.430697: clock-in

### 2020-03-29 17:00:11.285076: clock-out

* got multiple repos to render
Instead of repo.gitdir, the gitdir could be determined by the location of the hourly.yaml file.
That would allow compositions through a custom resolver:

```python
OmegaConf.register_resolver("repo", lambda cfg_file: OmegaConf.load(cfg_file).repo)
```

```yaml
repo: <conf>
report:
	repos:
		- ${repo:hourly.yaml}
		- ${repo:path/to/other/hourly.yaml}
```
Here, the resolver has to take into account user directories and relative paths

You may need to use the hydra decorator to pick up default args:
```python
hydra.main(config_path="conf/config.yaml", strict = True)
```


### 2020-03-29 14:18:59.040093: clock-in

### 2020-03-23 00:02:16.968108: clock-out

* using variable interpolation

### 2020-03-22 23:30:41.959084: clock-in

### 2020-03-21 23:01:56.800234: clock-out

* added repos option to report
* keeping repo option to specify the repo for clocking in/out

### 2020-03-21 22:16:11.776279: clock-in

### 2020-03-21 18:32:05.992784: clock-out

* we only want to clock in to the current repo and generate reports for all listed repos
* Listing multiple branches
* Using chdir for each listed repo

### 2020-03-21 17:05:31.416456: clock-in

### 2020-03-21 16:02:52.504923: clock-out


### 2020-03-21 15:48:39.355359: clock-in

### 2020-03-21 15:02:28.495820: clock-out

* The goal is to list multiple repos or branches in hourly's config.
* Hourly should be able to generate a timesheet that takes into account all listed branches/repos
* This feature will avoid cluttering a project's commit history with Hourly's metadata

### 2020-03-21 14:46:21.623353: clock-in

### 2020-03-14 20:41:54.111416: clock-out

* ENH - can run hourly commands from repo subdirectories
* test subdir
* version push
* testing hourly in subdir

### 2020-03-14 20:32:40.658394: clock-in

### Sat Mar 14 19:13:06 2020 -0500: clock-out
* had to clock out manually during wip

### 2020-03-14 18:56:34.870426: clock-in

### 2020-03-14 16:25:31.198516: clock-out

* hydra does not respect `os.chdir`!

### 2020-03-14 15:15:20.182542: clock-in

* fixing yaml includes for docs

### 2020-01-29 23:59:37.202116: clock-out

* fixed bug preventing users from clocking in

### 2020-01-29 23:45:29.962519: clock-in

### 2020-01-28 20:12:53.326321: clock-out

* fixed MANIFEST since cli moved into hourly module

### 2020-01-28 20:10:17.270214: clock-in

* fixed ignore bug preventing timesheet generation
* 0.3.10
* changed install path to hourly/cli

### 2020-01-14 19:02:53.559393: clock-out

* 0.3.9
* fixed timesheet filename bug

### 2020-01-14 18:47:30.370225: clock-in

* 0.3.8

### 2020-01-14 18:41:10.382420: clock-out

* fixed tminus
* code clean up
* switching to 'foo' in cfg.bar

### 2020-01-14 17:32:53.638696: clock-in

* pushing version
### 2020-01-14 02:30:57.609792: clock-out

* fixed bugs in invoice generation

### 2020-01-14 02:03:18.253023: clock-in

* trying to figure out submodules
### 2020-01-14 00:08:15.447796: clock-out

* minor doc changes
* updated remaining docs to reflect hourly-report
* changed README to reflect new hourly-report syntax
* fixed bug in invoice generation
* created hourly-report cli, cleaned up initialization code
* cli overrides broke grouping
* fixed bug where command line args were ignored by config_override
* turned off time sheet generation by default, updated README usage section

### 2020-01-13 22:01:00.641375: clock-in

* changing maxwidth again

### 2020-01-12 17:20:03.651580: clock-out

* changed earnings calculation to dictionary
* added verbosity setting, error handling
* moved invoicing code into their own module

### 2020-01-12 15:11:08.113248: clock-in

### 2020-01-12 09:40:04.640256: clock-out

* corrected MANIFEST.in path

### 2020-01-12 09:37:24.327410: clock-in

* removing Dashboard prototyping notebook

### 2020-01-12 09:06:00.564390: clock-out: T-20m 

* updated README intro

### 2020-01-12 08:23:25.178670: clock-in

### 2020-01-10 20:26:55.510181: clock-out


### 2020-01-10 20:23:24.001918: clock-in

### 2020-01-10 10:41:14.079277: clock-out

* simplifying btcpay setup
* updated btcpay config docs

### 2020-01-10 09:11:40.795394: clock-in

### 2020-01-09 23:55:09.691335: clock-out

* added work graph to WorkLog docs

### 2020-01-09 23:52:30.625119: clock-in

### 2020-01-09 23:30:09.366730: clock-out

* actually added MANIFEST.in this time
* updating docs

### 2020-01-09 22:22:01.026039: clock-in

* corrected invoice notification docs

### 2020-01-09 11:00:35.544185: clock-out

* added MANIFEST.in
* got hydra.errors.MissingConfigException on mac

### 2020-01-09 10:34:21.933690: clock-in

### 2020-01-09 09:19:01.967756: clock-out

* updated usage examples
* version update

### 2020-01-09 09:06:20.553382: clock-in

* adding stripe screen shot

### 2020-01-09 03:23:49.529611: clock-out

* added further install instructions

### 2020-01-09 03:22:04.616199: clock-in

* updating graph again.. I should really fix this

### 2020-01-09 02:59:24.294923: clock-out

* fixed up requirements

### 2020-01-09 02:47:45.455102: clock-in

* updated press release to include stripe
* redirected to Authors notes rather than email
* updating work graph

### 2020-01-09 02:35:00.616095: clock-out


### 2020-01-09 01:16:48.954647: clock-in

### 2020-01-09 01:14:18.157882: clock-out: T-10m 

* anonymized default stripe customer, changed invoice footer
* yo
* quieter logging from stripe api
* kept invoice config from sharing customer data between repos
* updated requirements.txt to include hydra
* fixed bug that raised error when only start or end given

### 2020-01-08 22:28:20.520139: clock-in

### 2020-01-08 03:36:04.021070: clock-out

* Got stripe integration!
* Refactored invoice configuration
* Simplified invoice command: `hourly invoice=btcpay` or `hourly invoice=stripe`

### 2020-01-08 00:05:07.910803: clock-in

### 2020-01-07 19:53:09.572565: clock-out

* started stripe integration
* added FAQ

### 2020-01-07 17:13:47.825366: clock-in: T-13m 

* updated compensation docs

### 2020-01-07 02:01:10.275284: clock-out

* attending announcement on bitcoinmeister show
* added documentation on compensation

### 2020-01-07 01:08:38.620674: clock-in

* pushing updated graph
* set plot hovermode to compare, updated docs

### 2020-01-07 00:26:37.876624: clock-out

* updated docs - added press release

### 2020-01-07 00:25:01.659294: clock-in: T-35m 

### 2020-01-06 23:49:06.433811: clock-out

* writing hourly blurb for bitcoin&markets newsletter
* updated configuration README

### 2020-01-06 23:03:59.405807: clock-in

* Need to send blurb to Ansel by friday, mention upwork, write up what you know about tradeoffs with lightning (costs, availability, etc)
* Need to add a gui and dockerize
* minor site fixes
* adding btcpay invoice screenshot
* fixed typo in docs, updated version
* touching up documentation
* updating work graph for hourly repo

### 2020-01-06 14:52:28.511302: clock-out

* merging with master
* BUGFIX force exit if btcpay-python not installed

### 2020-01-06 14:48:34.209232: clock-in: T-10m 

### 2020-01-06 00:57:44.096012: clock-out


### 2020-01-05 23:48:31.655464: clock-in: T-25m 

### 2020-01-05 23:22:17.765638: clock-out

* prompting user for confirmation
* renamed hourly-config.yaml to hourly.yaml

### 2020-01-05 21:17:55.844445: clock-in

### 2020-01-05 20:58:43.148966: clock-out

* documenting grouped config

### 2020-01-05 20:43:23.467637: clock-in

### 2020-01-05 17:34:41.710447: clock-out

* refactoring configuration using config groups
* does it make sense to be able to issue an invoice on behalf of someone else? 
* it's the responsibilty of the employer to make sure the invoice their getting is from the right person

### 2020-01-05 16:29:01.786457: clock-in

### 2020-01-05 16:03:22.389791: clock-out

* refactoring

### 2020-01-05 15:32:33.929020: clock-in

### 2020-01-05 02:59:59.550127: clock-out

* adding user_id to report.filename
* got hourly to issue first btcpayserver invoice!

### 2020-01-04 22:59:21.370595: clock-in

### 2020-01-04 20:06:20.516946: clock-out

* working with pem files
* changed default max column to match hash length

### 2020-01-04 18:56:53.105369: clock-in

### 2020-01-04 15:35:04.070440: clock-out

* moving invoice into cli
* setting up environment variable interpolation
* using OmegaConf.to_container(cfg) 
* cannot load a private key from environment variable on windows
* should probably use a private key file

### 2020-01-04 13:55:18.699752: clock-in

### 2020-01-04 13:01:43.289508: clock-out

* testing first invoice

### 2020-01-04 12:16:11.802771: clock-in

### 2020-01-03 21:40:56.858838: clock-out

* lightning payments

### 2020-01-03 19:45:54.790098: clock-in

### 2020-01-03 19:31:57.414479: clock-out

* looking at btcpayserver
* trying exitpay https://btc.exitpay.org/
* found exitpay confirmation email in spam folder

### 2020-01-03 17:44:04.019146: clock-in

* updating graph

### 2020-01-03 14:28:45.356496: clock-out

* addressing helpful hydra hints from Omry
* documentation improvements

### 2020-01-03 13:52:35.768769: clock-in

### 2020-01-02 18:53:49.974457: clock-out

* added ability to group timesheets by name or email or both
* fixed bug where user can accidentally clock in twice if a non-clock message is committed
* changed `report.outfile` to `report.filename`
* added multiple users to plot
* removed click app
* documentation updates

### 2020-01-02 14:42:06.286717: clock-in

### 2020-01-01 13:52:29.717923: clock-out

* adding ability to clock in multiple users
* check which email address is being used to clock in/out.

* `git config user.email` can be used to check which email is configured for the current repo
* can get name or email from author

### 2020-01-01 12:25:59.286809: clock-in

### 2019-12-31 14:54:48.254974: clock-out


### 2019-12-31 14:14:47.319391: clock-in

### 2019-12-30 15:23:56.531080: clock-out


### 2019-12-30 15:22:44.136505: clock-in

### 2019-12-30 15:22:18.590328: clock-out

* documentation and hydra code push
* cleaned up output for `clock-in` and `clock-out` messages
* updated documentation site to reflect move to hydra

### 2019-12-30 12:17:38.426420: clock-in

### 2019-12-29 22:28:23.663515: clock-out

switching from click to hydra involves some caveats. 
I really dislike the practice of deprecation, which often breaks things that didn't need fixing. 
My goal is to minimize that pain for users of the old app. To that end:

* keep existing cli while in development to ensure behavior can be replicated
* create a unique (temporary?) name for new app (e.g. myapp-hydra or myapp-cli)
* replace common flags with separate cli tools. For instance, `myapp -myflag` becomes `myapp-myflag`,
where `myapp-myflag` wraps the interface `myapp-cli myflag=true`

This last one means there is actually one *less* character to write.

* added dictConfig_to_dict function to recursively construct nested dict
* pandas.set_option takes names like `display.max_colwidth`
* got hourly-in, hourly-out functional
* not sure how to make command-line inputs override `config_override` setting

### 2019-12-29 19:42:03.967359: clock-in

### 2019-12-29 18:02:55.046177: clock-out
* developing cli with hydra

### 2019-12-29 16:34:02.562291: clock-in

### 2019-12-26 13:05:03.226272: clock-out
* working on refactoring cli with new config
* adding ability to commit messages without clocking
* user should not have to directly edit work log

### 2019-12-26 11:41:13.289307: clock-in

### 2019-12-23 13:42:32.292273: clock-out
* switching to hydra this changes the cli from `hourly -in` to `hourly commit.clock=in`
* finished up the first iteration of the cli spec!

### 2019-12-23 12:06:57.928740: clock-in: T-30m

### 2019-12-01 13:21:31.816735: clock-out
* trying out different plot options
* looking into configuration setup

### 2019-12-01 12:50:42.892528: clock-in

### 2019-11-30 16:19:45.897554: clock-out
* embedding work graph as iframe
* changing `--plot` option to specify path/to/work-graph.html

### 2019-11-30 15:25:51.433329: clock-in

### 2019-11-30 15:07:32.727339: clock-out
* Testing header depth option

### 2019-11-30 15:05:34.680440: clock-in

### 2019-11-30 14:58:11.651795: clock-out
* updating docs
* added worklog header depth option 

### 2019-11-30 13:53:43.831968: clock-in

### 2019-10-23 22:55:48.632734: clock-out

### 2019-10-23 21:10:25.808038: clock-in

### 2019-09-19 21:47:37.949509: clock-out

* Moved time adjustment so it only applies at labor calculation, in clock commits

### 2019-09-19 21:13:46.261481: clock-in

### 2019-09-19 20:43:24.455285: clock-out
* pysat contains commits with ROCSAT-1, which breaks time adjustment

### 2019-09-19 20:33:26.659734: clock-in

### 2019-09-19 20:25:52.236443: clock-out
* testing on pysat repo

### 2019-09-19 20:18:01.673816: clock-in

### 2019-08-21 01:17:15.009128: clock-out: added plot options
* add plot output

### 2019-08-20 23:21:41.235199: clock-in

### 2019-08-14 00:30:48.962283: clock-out
* failed to fix utc error when giving only start time

### 2019-08-14 00:12:41.780463: clock-in: T-7m

### 2019-08-14 00:05:12.536012: clock-out
* Testing new output for double clock in warning

### 2019-08-14 00:04:16.778490: clock-in

### 2019-08-14 00:04:04.274688: clock-out

### 2019-08-14 00:03:57.681741: clock-in: T-1h22m

### 2019-08-13 22:40:45.276268: clock-out
* bug: negative dt when listing work for one day
* UTC bug occurs when no end date is specified
* removed default from wage option
* Got table into gui

### 2019-08-13 22:39:42.742055: clock-in

### 2019-08-07 23:51:23.947759: clock-out: T-15m
* upgrading to python 3.7
* cleaned up output for when no labor is available
* prototyping gui
* bug when date range covers different UTC offsets, which can occur during travel:

```console
2018-10-28 13:44:48-04:00                              clock in  c4e95f59dc0c8ce296a40300760ab6880...
2018-10-28 13:56:35-04:00                             clock out  f5200e718c062e828d436506286fd05e5...
2019-02-25 10:19:10-05:00                        clock in T-1hr  d7add63b4d2e3e1ca1423296aaed25d9c...
2019-02-25 12:49:51-05:00                        clock out T-5m  acfb8596317786e38177345aa25310980...
2019-03-10 22:57:58-04:00                              clock in  217ad6169fbd10efbb1e497a6cc6e4553...
2019-03-11 00:05:42-04:00  clock out - integrating with read...  297a561d5d7c57ecb641fa841d86dc5a6...
```

### 2019-08-07 22:01:03.125488: clock-in

### 2019-06-19 19:03:19.375329: clock-out

### 2019-06-19 18:11:54.185775: clock-in

### 2019-06-19 14:56:37.451578: clock-out: T-5m
* Weasyprint looks like the easiest path to generating pdfs
* Look at their [invoice](https://github.com/Kozea/WeasyPrint/tree/gh-pages/samples/invoice) example

### 2019-06-19 14:32:23.261121: clock-in

### 2019-06-13 18:36:23.538048: clock-out
* Looking at generating invoices in pdf

### 2019-06-13 18:19:19.036767: clock-in

### 2019-04-17 00:21:48.211640: clock-out

* got c-lightning server running in container on windows 10
* had to skip the -u `id -u` parameter, which means it runs as root
* have to use docker-machine ip to get the appropriate ip for the windows container
* got a few of the rest api commands to work, then ran into this:

	Starting bitcoind... waiting for cookie... waiting for RPC... Error: Error: Disk space is low!

* may need to delete ./data and start again?

### 2019-04-16 23:06:17.688503: clock-in: researching payments

### 2019-04-16 01:21:50.338638: clock-out

* Looking into lightning payments https://github.com/ElementsProject/lightning-charge

### 2019-04-16 00:01:09.069912: clock-in

### 2019-04-13 02:43:19.905950: clock-out

* Looking into payment automation
* fixed an errant clock-in/out with hard reset:

	git reset --hard 590804df784c45051c548eb84e930c1157d6acc1

Where I used the last clock-out commit hash from 2019-04-12 18:04:27.744011

### 2019-04-13 02:24:44.339725: clock-in: T-45m

### 2019-04-12 18:04:27.744011: clock-out

### 2019-04-12 17:53:58.904877: clock-in: payment options

### 2019-04-12 15:45:54.653421: clock-out
* determine why report sometimes shows negative time deltas

### 2019-04-12 15:41:12.003763: clock-in

### 2019-04-11 02:48:43.722703: clock-out
### Apr 11, 2019

* Finished in/out flags

### Apr 8, 2019

* working on in/out flags

### Apr 7, 2019

* Adding "hourly in/out" flags
* Pushing python 3 version
* Looking into payment options

### Mar 15, 2019

* Fixed issue with ignore default

### Mar 14, 2019

* bug fixing

### Mar 12, 2019

* scrapping readthedocs in favor of github.io
* starting command-line interface

### Mar 11, 2019

* Trying to fix build error


### Mar 10, 2019

* Added documentation site
* Started integration with readthedocs


### Feb 25, 2019

* Added clock adjustments
* Made match_logs option to raise an error when in/out clocks don't match


### Oct 20, 2018

* Switched to pd.Timestamp to allow for easier slicing
* Added timezones
* Notebook Tutorial runs without errors


### Oct 28, 2018

=======
### 2021-11-04 22:50:59.524021: clock-out


### 2021-11-04 20:08:51.896212: clock-in

### 2021-10-19 04:03:29.521261: clock-out

* sorting by time
* fixed button children, buttons working

### 2021-10-19 03:24:24.827527: clock-in

### 2021-10-19 03:24:16.778547: clock-out

* clicking clock out button should changed "clocked in" button to "clock in"

### 2021-10-19 03:19:01.435458: clock-in

### 2021-10-19 03:18:53.143795: clock-out


### 2021-10-19 03:16:26.428876: clock-in

### 2021-10-19 03:16:05.150957: clock-out


### 2021-10-19 03:07:01.424080: clock-in

### 2021-10-19 02:15:19.311658: clock-out


### 2021-10-18 21:00:00.665679: clock-in

### 2021-10-17 23:24:57.991280: clock-out

* commit author
* added tabs, commit author

### 2021-10-18 04:21:49.851718: clock-in

### 2021-10-18 04:20:26.553289: clock-out

### 2021-10-18 03:57:38.837050: clock-out


### 2021-10-17 22:07:11.281903: clock-in

### 2021-10-17 16:25:23.021970: clock-out


### 2021-10-17 15:37:55.248115: clock-in

### 2021-09-30 21:18:36.224621: clock-out

* adding inout to dashboard
* `process_commit` needs to use registered id

### 2021-09-30 19:26:53.261218: clock-in

### 2021-09-30 00:04:21.838617: clock-out

* separate in/out buttons

### 2021-09-29 23:22:58.657224: clock-in

### 2021-09-28 23:57:52.543075: clock-out

* trying toggle switch

### 2021-09-28 23:25:14.324913: clock-in

### 2021-09-27 23:18:48.655650: clock-out

* basic layout, clock in/out counter

### 2021-09-27 21:31:42.053205: clock-in

### 2021-09-27 21:09:01.740071: clock-out


### 2021-09-27 21:03:33.790613: clock-in
=======
### 2021-11-10 14:20:31.719466: clock-out

* fixed bug in timezone filter
* moving worklog
* getting the following issue when changed timezones:

```sh
hourly-report repo.start_date="Aug 1, 2021"

...

raise KeyError(orig_key) from err
KeyError: Timestamp('2021-08-01 01:00:00-0400', tz='US/Eastern')
```

### 2021-11-10 13:37:16.749040: clock-in: T-28m 


### 2021-09-26 22:33:15.023326: clock-out

* version push

### 2021-09-26 22:32:43.479051: clock-in: T-30m 

### 2021-09-26 13:48:59.580563: clock-out

* merging multi-repo-conf
* merging multi-repo-conf
* fixed timedelta bug
* BUG fixed required clock statement
* BUG fixed time shift update
* moving into worklogs
* saw this when clocking in

`rosetta error: ThreadContext::resume failed 4`

### 2021-09-26 13:13:08.492389: clock-in

### 2021-07-23 01:06:09.646169: clock-out

* fixed time adjustment with message bug

### 2021-07-22 22:52:16.602663: clock-in

* removing requirements file
### 2021-05-15 16:17:11.997280: clock-out

* added bugfix for multi named repos

### 2021-05-15 16:16:43.647226: clock-in

### 2021-05-15 16:07:06.595128: clock-out: T-20m 

* bug preventing multiple names from adding across multiple repos

### 2021-05-15 15:15:48.282768: clock-in

### 2021-04-06 00:20:14.862558: clock-out

* added division of labor for multiple repo names

### 2021-04-05 22:00:06.101441: clock-in

### 2020-08-07 11:57:14.484755: clock-out

* added normalization without second axis

### 2020-08-07 11:32:29.729332: clock-in

### 2020-07-29 20:42:30.976371: clock-out

* added average time

### 2020-07-29 19:09:05.013725: clock-in: T-30m 

### 2020-07-29 17:32:59.062285: clock-out


### 2020-07-29 17:03:52.631490: clock-in

* fixed tz localize error
* fixed timedelta update again
* fixing time adjustment
### 2020-04-05 23:12:17.506294: clock-out

* got groupings to work by name or repo

### 2020-04-05 23:10:16.904078: clock-in: T-30m 

### 2020-04-05 22:33:49.515939: clock-out: T-5h 


### 2020-04-05 17:27:29.678827: clock-in

### 2020-04-05 13:51:53.130898: clock-out

* bug fixes

### 2020-04-05 13:36:21.847920: clock-in

### 2020-04-05 13:18:53.515173: clock-out

* fixing bugs not allowing group by name

### 2020-04-05 12:06:16.000383: clock-in

### 2020-04-05 11:05:49.617937: clock-out

* grouping by name

### 2020-04-05 11:00:51.458868: clock-in

* updating multi repo docs
### 2020-04-05 00:22:24.450956: clock-out: T-10m 

* adding multi repo docs

### 2020-04-04 23:20:09.144648: clock-in

### 2020-04-04 15:12:34.630127: clock-out

* added 'report.grouping' to specify name, email, repo, branch
* got multiple branches to work
* moved cli arg override into config_override
* fixed bug preventing command line args from overriding those specified in config_override

### 2020-04-04 12:38:56.777222: clock-in

### 2020-04-01 16:50:06.390562: clock-out

* set default repo name to empty str (pandas groupby ignores `None` values)

### 2020-04-01 16:32:39.430697: clock-in

### 2020-03-29 17:00:11.285076: clock-out

* got multiple repos to render
Instead of repo.gitdir, the gitdir could be determined by the location of the hourly.yaml file.
That would allow compositions through a custom resolver:

```python
OmegaConf.register_resolver("repo", lambda cfg_file: OmegaConf.load(cfg_file).repo)
```

```yaml
repo: <conf>
report:
	repos:
		- ${repo:hourly.yaml}
		- ${repo:path/to/other/hourly.yaml}
```
Here, the resolver has to take into account user directories and relative paths

You may need to use the hydra decorator to pick up default args:
```python
hydra.main(config_path="conf/config.yaml", strict = True)
```


### 2020-03-29 14:18:59.040093: clock-in

### 2020-03-23 00:02:16.968108: clock-out

* using variable interpolation

### 2020-03-22 23:30:41.959084: clock-in

### 2020-03-21 23:01:56.800234: clock-out

* added repos option to report
* keeping repo option to specify the repo for clocking in/out

### 2020-03-21 22:16:11.776279: clock-in

### 2020-03-21 18:32:05.992784: clock-out

* we only want to clock in to the current repo and generate reports for all listed repos
* Listing multiple branches
* Using chdir for each listed repo

### 2020-03-21 17:05:31.416456: clock-in

### 2020-03-21 16:02:52.504923: clock-out


### 2020-03-21 15:48:39.355359: clock-in

### 2020-03-21 15:02:28.495820: clock-out

* The goal is to list multiple repos or branches in hourly's config.
* Hourly should be able to generate a timesheet that takes into account all listed branches/repos
* This feature will avoid cluttering a project's commit history with Hourly's metadata

### 2020-03-21 14:46:21.623353: clock-in

### 2020-03-14 20:41:54.111416: clock-out

* ENH - can run hourly commands from repo subdirectories
* test subdir
* version push
* testing hourly in subdir

### 2020-03-14 20:32:40.658394: clock-in

### Sat Mar 14 19:13:06 2020 -0500: clock-out
* had to clock out manually during wip

### 2020-03-14 18:56:34.870426: clock-in

### 2020-03-14 16:25:31.198516: clock-out

* hydra does not respect `os.chdir`!

### 2020-03-14 15:15:20.182542: clock-in

* fixing yaml includes for docs

### 2020-01-29 23:59:37.202116: clock-out

* fixed bug preventing users from clocking in

### 2020-01-29 23:45:29.962519: clock-in

### 2020-01-28 20:12:53.326321: clock-out

* fixed MANIFEST since cli moved into hourly module

### 2020-01-28 20:10:17.270214: clock-in

* fixed ignore bug preventing timesheet generation
* 0.3.10
* changed install path to hourly/cli

### 2020-01-14 19:02:53.559393: clock-out

* 0.3.9
* fixed timesheet filename bug

### 2020-01-14 18:47:30.370225: clock-in

* 0.3.8

### 2020-01-14 18:41:10.382420: clock-out

* fixed tminus
* code clean up
* switching to 'foo' in cfg.bar

### 2020-01-14 17:32:53.638696: clock-in

* pushing version
### 2020-01-14 02:30:57.609792: clock-out

* fixed bugs in invoice generation

### 2020-01-14 02:03:18.253023: clock-in

* trying to figure out submodules
### 2020-01-14 00:08:15.447796: clock-out

* minor doc changes
* updated remaining docs to reflect hourly-report
* changed README to reflect new hourly-report syntax
* fixed bug in invoice generation
* created hourly-report cli, cleaned up initialization code
* cli overrides broke grouping
* fixed bug where command line args were ignored by config_override
* turned off time sheet generation by default, updated README usage section

### 2020-01-13 22:01:00.641375: clock-in

* changing maxwidth again

### 2020-01-12 17:20:03.651580: clock-out

* changed earnings calculation to dictionary
* added verbosity setting, error handling
* moved invoicing code into their own module

### 2020-01-12 15:11:08.113248: clock-in

### 2020-01-12 09:40:04.640256: clock-out

* corrected MANIFEST.in path

### 2020-01-12 09:37:24.327410: clock-in

* removing Dashboard prototyping notebook

### 2020-01-12 09:06:00.564390: clock-out: T-20m 

* updated README intro

### 2020-01-12 08:23:25.178670: clock-in

### 2020-01-10 20:26:55.510181: clock-out


### 2020-01-10 20:23:24.001918: clock-in

### 2020-01-10 10:41:14.079277: clock-out

* simplifying btcpay setup
* updated btcpay config docs

### 2020-01-10 09:11:40.795394: clock-in

### 2020-01-09 23:55:09.691335: clock-out

* added work graph to WorkLog docs

### 2020-01-09 23:52:30.625119: clock-in

### 2020-01-09 23:30:09.366730: clock-out

* actually added MANIFEST.in this time
* updating docs

### 2020-01-09 22:22:01.026039: clock-in

* corrected invoice notification docs

### 2020-01-09 11:00:35.544185: clock-out

* added MANIFEST.in
* got hydra.errors.MissingConfigException on mac

### 2020-01-09 10:34:21.933690: clock-in

### 2020-01-09 09:19:01.967756: clock-out

* updated usage examples
* version update

### 2020-01-09 09:06:20.553382: clock-in

* adding stripe screen shot

### 2020-01-09 03:23:49.529611: clock-out

* added further install instructions

### 2020-01-09 03:22:04.616199: clock-in

* updating graph again.. I should really fix this

### 2020-01-09 02:59:24.294923: clock-out

* fixed up requirements

### 2020-01-09 02:47:45.455102: clock-in

* updated press release to include stripe
* redirected to Authors notes rather than email
* updating work graph

### 2020-01-09 02:35:00.616095: clock-out


### 2020-01-09 01:16:48.954647: clock-in

### 2020-01-09 01:14:18.157882: clock-out: T-10m 

* anonymized default stripe customer, changed invoice footer
* yo
* quieter logging from stripe api
* kept invoice config from sharing customer data between repos
* updated requirements.txt to include hydra
* fixed bug that raised error when only start or end given

### 2020-01-08 22:28:20.520139: clock-in

### 2020-01-08 03:36:04.021070: clock-out

* Got stripe integration!
* Refactored invoice configuration
* Simplified invoice command: `hourly invoice=btcpay` or `hourly invoice=stripe`

### 2020-01-08 00:05:07.910803: clock-in

### 2020-01-07 19:53:09.572565: clock-out

* started stripe integration
* added FAQ

### 2020-01-07 17:13:47.825366: clock-in: T-13m 

* updated compensation docs

### 2020-01-07 02:01:10.275284: clock-out

* attending announcement on bitcoinmeister show
* added documentation on compensation

### 2020-01-07 01:08:38.620674: clock-in

* pushing updated graph
* set plot hovermode to compare, updated docs

### 2020-01-07 00:26:37.876624: clock-out

* updated docs - added press release

### 2020-01-07 00:25:01.659294: clock-in: T-35m 

### 2020-01-06 23:49:06.433811: clock-out

* writing hourly blurb for bitcoin&markets newsletter
* updated configuration README

### 2020-01-06 23:03:59.405807: clock-in

* Need to send blurb to Ansel by friday, mention upwork, write up what you know about tradeoffs with lightning (costs, availability, etc)
* Need to add a gui and dockerize
* minor site fixes
* adding btcpay invoice screenshot
* fixed typo in docs, updated version
* touching up documentation
* updating work graph for hourly repo

### 2020-01-06 14:52:28.511302: clock-out

* merging with master
* BUGFIX force exit if btcpay-python not installed

### 2020-01-06 14:48:34.209232: clock-in: T-10m 

### 2020-01-06 00:57:44.096012: clock-out


### 2020-01-05 23:48:31.655464: clock-in: T-25m 

### 2020-01-05 23:22:17.765638: clock-out

* prompting user for confirmation
* renamed hourly-config.yaml to hourly.yaml

### 2020-01-05 21:17:55.844445: clock-in

### 2020-01-05 20:58:43.148966: clock-out

* documenting grouped config

### 2020-01-05 20:43:23.467637: clock-in

### 2020-01-05 17:34:41.710447: clock-out

* refactoring configuration using config groups
* does it make sense to be able to issue an invoice on behalf of someone else? 
* it's the responsibilty of the employer to make sure the invoice their getting is from the right person

### 2020-01-05 16:29:01.786457: clock-in

### 2020-01-05 16:03:22.389791: clock-out

* refactoring

### 2020-01-05 15:32:33.929020: clock-in

### 2020-01-05 02:59:59.550127: clock-out

* adding user_id to report.filename
* got hourly to issue first btcpayserver invoice!

### 2020-01-04 22:59:21.370595: clock-in

### 2020-01-04 20:06:20.516946: clock-out

* working with pem files
* changed default max column to match hash length

### 2020-01-04 18:56:53.105369: clock-in

### 2020-01-04 15:35:04.070440: clock-out

* moving invoice into cli
* setting up environment variable interpolation
* using OmegaConf.to_container(cfg) 
* cannot load a private key from environment variable on windows
* should probably use a private key file

### 2020-01-04 13:55:18.699752: clock-in

### 2020-01-04 13:01:43.289508: clock-out

* testing first invoice

### 2020-01-04 12:16:11.802771: clock-in

### 2020-01-03 21:40:56.858838: clock-out

* lightning payments

### 2020-01-03 19:45:54.790098: clock-in

### 2020-01-03 19:31:57.414479: clock-out

* looking at btcpayserver
* trying exitpay https://btc.exitpay.org/
* found exitpay confirmation email in spam folder

### 2020-01-03 17:44:04.019146: clock-in

* updating graph

### 2020-01-03 14:28:45.356496: clock-out

* addressing helpful hydra hints from Omry
* documentation improvements

### 2020-01-03 13:52:35.768769: clock-in

### 2020-01-02 18:53:49.974457: clock-out

* added ability to group timesheets by name or email or both
* fixed bug where user can accidentally clock in twice if a non-clock message is committed
* changed `report.outfile` to `report.filename`
* added multiple users to plot
* removed click app
* documentation updates

### 2020-01-02 14:42:06.286717: clock-in

### 2020-01-01 13:52:29.717923: clock-out

* adding ability to clock in multiple users
* check which email address is being used to clock in/out.

* `git config user.email` can be used to check which email is configured for the current repo
* can get name or email from author

### 2020-01-01 12:25:59.286809: clock-in

### 2019-12-31 14:54:48.254974: clock-out


### 2019-12-31 14:14:47.319391: clock-in

### 2019-12-30 15:23:56.531080: clock-out


### 2019-12-30 15:22:44.136505: clock-in

### 2019-12-30 15:22:18.590328: clock-out

* documentation and hydra code push
* cleaned up output for `clock-in` and `clock-out` messages
* updated documentation site to reflect move to hydra

### 2019-12-30 12:17:38.426420: clock-in

### 2019-12-29 22:28:23.663515: clock-out

switching from click to hydra involves some caveats. 
I really dislike the practice of deprecation, which often breaks things that didn't need fixing. 
My goal is to minimize that pain for users of the old app. To that end:

* keep existing cli while in development to ensure behavior can be replicated
* create a unique (temporary?) name for new app (e.g. myapp-hydra or myapp-cli)
* replace common flags with separate cli tools. For instance, `myapp -myflag` becomes `myapp-myflag`,
where `myapp-myflag` wraps the interface `myapp-cli myflag=true`

This last one means there is actually one *less* character to write.

* added dictConfig_to_dict function to recursively construct nested dict
* pandas.set_option takes names like `display.max_colwidth`
* got hourly-in, hourly-out functional
* not sure how to make command-line inputs override `config_override` setting

### 2019-12-29 19:42:03.967359: clock-in

### 2019-12-29 18:02:55.046177: clock-out
* developing cli with hydra

### 2019-12-29 16:34:02.562291: clock-in

### 2019-12-26 13:05:03.226272: clock-out
* working on refactoring cli with new config
* adding ability to commit messages without clocking
* user should not have to directly edit work log

### 2019-12-26 11:41:13.289307: clock-in

### 2019-12-23 13:42:32.292273: clock-out
* switching to hydra this changes the cli from `hourly -in` to `hourly commit.clock=in`
* finished up the first iteration of the cli spec!

### 2019-12-23 12:06:57.928740: clock-in: T-30m

### 2019-12-01 13:21:31.816735: clock-out
* trying out different plot options
* looking into configuration setup

### 2019-12-01 12:50:42.892528: clock-in

### 2019-11-30 16:19:45.897554: clock-out
* embedding work graph as iframe
* changing `--plot` option to specify path/to/work-graph.html

### 2019-11-30 15:25:51.433329: clock-in

### 2019-11-30 15:07:32.727339: clock-out
* Testing header depth option

### 2019-11-30 15:05:34.680440: clock-in

### 2019-11-30 14:58:11.651795: clock-out
* updating docs
* added worklog header depth option 

### 2019-11-30 13:53:43.831968: clock-in

### 2019-10-23 22:55:48.632734: clock-out

### 2019-10-23 21:10:25.808038: clock-in

### 2019-09-19 21:47:37.949509: clock-out

* Moved time adjustment so it only applies at labor calculation, in clock commits

### 2019-09-19 21:13:46.261481: clock-in

### 2019-09-19 20:43:24.455285: clock-out
* pysat contains commits with ROCSAT-1, which breaks time adjustment

### 2019-09-19 20:33:26.659734: clock-in

### 2019-09-19 20:25:52.236443: clock-out
* testing on pysat repo

### 2019-09-19 20:18:01.673816: clock-in

### 2019-08-21 01:17:15.009128: clock-out: added plot options
* add plot output

### 2019-08-20 23:21:41.235199: clock-in

### 2019-08-14 00:30:48.962283: clock-out
* failed to fix utc error when giving only start time

### 2019-08-14 00:12:41.780463: clock-in: T-7m

### 2019-08-14 00:05:12.536012: clock-out
* Testing new output for double clock in warning

### 2019-08-14 00:04:16.778490: clock-in

### 2019-08-14 00:04:04.274688: clock-out

### 2019-08-14 00:03:57.681741: clock-in: T-1h22m

### 2019-08-13 22:40:45.276268: clock-out
* bug: negative dt when listing work for one day
* UTC bug occurs when no end date is specified
* removed default from wage option
* Got table into gui

### 2019-08-13 22:39:42.742055: clock-in

### 2019-08-07 23:51:23.947759: clock-out: T-15m
* upgrading to python 3.7
* cleaned up output for when no labor is available
* prototyping gui
* bug when date range covers different UTC offsets, which can occur during travel:

```console
2018-10-28 13:44:48-04:00                              clock in  c4e95f59dc0c8ce296a40300760ab6880...
2018-10-28 13:56:35-04:00                             clock out  f5200e718c062e828d436506286fd05e5...
2019-02-25 10:19:10-05:00                        clock in T-1hr  d7add63b4d2e3e1ca1423296aaed25d9c...
2019-02-25 12:49:51-05:00                        clock out T-5m  acfb8596317786e38177345aa25310980...
2019-03-10 22:57:58-04:00                              clock in  217ad6169fbd10efbb1e497a6cc6e4553...
2019-03-11 00:05:42-04:00  clock out - integrating with read...  297a561d5d7c57ecb641fa841d86dc5a6...
```

### 2019-08-07 22:01:03.125488: clock-in

### 2019-06-19 19:03:19.375329: clock-out

### 2019-06-19 18:11:54.185775: clock-in

### 2019-06-19 14:56:37.451578: clock-out: T-5m
* Weasyprint looks like the easiest path to generating pdfs
* Look at their [invoice](https://github.com/Kozea/WeasyPrint/tree/gh-pages/samples/invoice) example

### 2019-06-19 14:32:23.261121: clock-in

### 2019-06-13 18:36:23.538048: clock-out
* Looking at generating invoices in pdf

### 2019-06-13 18:19:19.036767: clock-in

### 2019-04-17 00:21:48.211640: clock-out

* got c-lightning server running in container on windows 10
* had to skip the -u `id -u` parameter, which means it runs as root
* have to use docker-machine ip to get the appropriate ip for the windows container
* got a few of the rest api commands to work, then ran into this:

	Starting bitcoind... waiting for cookie... waiting for RPC... Error: Error: Disk space is low!

* may need to delete ./data and start again?

### 2019-04-16 23:06:17.688503: clock-in: researching payments

### 2019-04-16 01:21:50.338638: clock-out

* Looking into lightning payments https://github.com/ElementsProject/lightning-charge

### 2019-04-16 00:01:09.069912: clock-in

### 2019-04-13 02:43:19.905950: clock-out

* Looking into payment automation
* fixed an errant clock-in/out with hard reset:

	git reset --hard 590804df784c45051c548eb84e930c1157d6acc1

Where I used the last clock-out commit hash from 2019-04-12 18:04:27.744011

### 2019-04-13 02:24:44.339725: clock-in: T-45m

### 2019-04-12 18:04:27.744011: clock-out

### 2019-04-12 17:53:58.904877: clock-in: payment options

### 2019-04-12 15:45:54.653421: clock-out
* determine why report sometimes shows negative time deltas

### 2019-04-12 15:41:12.003763: clock-in

### 2019-04-11 02:48:43.722703: clock-out
### Apr 11, 2019

* Finished in/out flags

### Apr 8, 2019

* working on in/out flags

### Apr 7, 2019

* Adding "hourly in/out" flags
* Pushing python 3 version
* Looking into payment options

### Mar 15, 2019

* Fixed issue with ignore default

### Mar 14, 2019

* bug fixing

### Mar 12, 2019

* scrapping readthedocs in favor of github.io
* starting command-line interface

### Mar 11, 2019

* Trying to fix build error


### Mar 10, 2019

* Added documentation site
* Started integration with readthedocs


### Feb 25, 2019

* Added clock adjustments
* Made match_logs option to raise an error when in/out clocks don't match


### Oct 20, 2018

* Switched to pd.Timestamp to allow for easier slicing
* Added timezones
* Notebook Tutorial runs without errors


### Oct 28, 2018

* Removed line breaks from report
// Node.js libraries
import events from 'events';
import util from 'util';

// Our modules
import Request from './Request';
import RedditRequest from './RedditRequest';
import Throttle from './Throttle';
import UserConfig from './UserConfig';
import OAuth from './OAuth';
import Modhash from './Modhash';
import fileHelper from './https/file';

export default class Snoocore extends events.EventEmitter {

  static get version() {
    return '3.2.0';
  }

  static file(...args) {
    return fileHelper(...args);
  }

  constructor(userConfiguration) {
    super();

    // @TODO - this is a "god object" of sorts.
    this._userConfig = new UserConfig(userConfiguration);

    this._throttle = new Throttle(this._userConfig.throttle);

    this._request = new Request(this._throttle);

    this._request.on('response_error', (responseError) => {
      this.emit('response_error', responseError);
    });

    // Two OAuth instances. One for authenticated users, and another for
    // Application only OAuth. Two are needed in the instance where
    // a user wants to bypass authentication for a call - we don't want
    // to waste time by creating a new app only instance, authenticating,
    // etc.
    this.oauth = new OAuth(this._userConfig, this._request);
    this.oauthAppOnly = new OAuth(this._userConfig, this._request);

    // Expose OAuth functions in here
    [ 'getExplicitAuthUrl',
      'getImplicitAuthUrl',
      'getAuthUrl',
      'auth',
      'refresh',
      'deauth',
      'getRefreshToken',
      'getAccessToken',
      'setRefreshToken',
      'setAccessToken',
      'hasRefreshToken',
      'hasAccessToken'
    ].forEach(fn => { this[fn] = this.oauth[fn].bind(this.oauth); });

    if (this._userConfig.useBrowserCookies) {
      this.modhash = new Modhash(this._userConfig, this._request);

      // Expose Modhash functions in here
      [ 'isModhashOld',
        'setModhash',
        'getModhash',
        'getCurrentModhash',
        'refreshModhash'
      ].forEach(fn => { this[fn] = this.modhash[fn].bind(this.modhash); });
    }

    this.appOnlyAuth = this.oauthAppOnly.applicationOnlyAuth.bind(this.oauthAppOnly);

    // Bubble up the  events
    this.oauth.on('access_token_refreshed', (accessToken) => {
      this.emit('access_token_refreshed', accessToken);
    });


    this._redditRequest = new RedditRequest(this._userConfig,
                                            this._request,
                                            this.oauth,
                                            this.oauthAppOnly,
                                            this.modhash);

    this._redditRequest.on('access_token_expired', (responseError) => {
      this.emit('access_token_expired', responseError);
    });

    this._redditRequest.on('rate_limit', (rateLimitData) => {
      this.emit('rate_limit', rateLimitData);
    });

    this._redditRequest.on('rate_limit_reached', (rateLimitData) => {
      // let the user know that they have gone over
      this.emit('rate_limit_reached', rateLimitData);
      // Delay the next call until the rate limit reset occurs
      this._throttle.addTime(rateLimitData.rateLimitReset * 1000);
    });

    /*
       Make this._redditRequest.path the primary function that we return, but
       stick the rest of the available functions on the prototype so we
       can use them as well.
     */
    let path = this._redditRequest.path.bind(this._redditRequest);

    let key;
    for (key in this) {
      path[key] = this[key];
    }

    return path;
  }
}

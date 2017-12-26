
import { Injectable } from '@angular/core';

@Injectable()
export class Configuration {
    public Server = 'http://127.0.0.1:8015';
    public ApiUrl = '/albums';
    public ServerWithApiUrl = this.Server + this.ApiUrl;
}
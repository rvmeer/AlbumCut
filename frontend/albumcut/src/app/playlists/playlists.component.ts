import { Component, OnInit } from '@angular/core';

import { DataService } from '../shared/dataService';

@Component({
  selector: 'app-playlists',
  templateUrl: './playlists.component.html',
  styleUrls: ['./playlists.component.css']
})
export class PlaylistsComponent implements OnInit {

  public message: string;
  public playlists: Playlist[];

    constructor(
        private _dataService: DataService) {
       
        
        
    }

  ngOnInit() {
    
        this._dataService
            .getAll<Playlist[]>('playlists')
            .subscribe((data: Playlist[]) => this.playlists = data,
            error => () => {
                this.message = 'Error!';
            },
            () => {
                this.message = 'OK';
            });
    }

}

class Playlist{
	public id: string;
	public name: string;
	public uri: string;

	public constructor(id: string, name: string){
		this.id = id;
		this.name = name;
	}
}

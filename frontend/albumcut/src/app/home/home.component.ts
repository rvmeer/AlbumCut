import { Component, OnInit } from '@angular/core';
import { DataService } from '../shared/dataService';

@Component({
    selector: 'app-home-component',
    templateUrl: './home.component.html'
})

export class HomeComponent implements OnInit {

    public message: string;
    public albums: Album[];

    constructor(
        private _dataService: DataService) {
       
        this.message = 'Hello from HomeComponent constructor';
        
        
    }

    ngOnInit() {
    
        this._dataService
            .getAll<Album[]>()
            .subscribe((data: Album[]) => this.albums = data,
            error => () => {
                this.message = 'Error!';
            },
            () => {
                this.message = 'OK';
            });
    }
}

class Album{
	public id: string;
	public name: string;
	public uri: string;

	public constructor(id: string, name: string){
		this.id = id;
		this.name = name;
	}
}
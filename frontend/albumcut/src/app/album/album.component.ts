import { Component, Input} from '@angular/core';
import { DataService } from '../shared/dataService';
import { Album } from '../shared/models';

@Component({
  selector: 'app-album',
  templateUrl: './album.component.html',
  styleUrls: ['./album.component.css']
})
export class AlbumComponent {

  @Input() album: Album;
  
 
  	

    getArtistName(): string{
    	return this.album && this.album.artists && this.album.artists.length>0 && this.album.artists[0].name || null;
    }
}
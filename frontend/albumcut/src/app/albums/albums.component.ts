import { Component, Input } from '@angular/core';
import { Album } from '../shared/models';
import { AlbumComponent} from '../album/album.component';

@Component({
  selector: 'app-albums',
  templateUrl: './albums.component.html',
  styleUrls: ['./albums.component.css']
  
})
export class AlbumsComponent  {
	
  @Input() albums: Album[];

   

  

    public getSmallImageUrl(album: Album):string {
        return album.getSmallImageUrl();
    }

}

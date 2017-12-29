import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';


import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { Configuration } from './app.constants';
import { SharedModule } from './shared/shared.module';
import { HttpClientModule } from '@angular/common/http';

// ngx-bootstrap
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { ModalModule } from 'ngx-bootstrap/modal';
import { TabsModule } from 'ngx-bootstrap/tabs';
import { AccordionModule } from 'ngx-bootstrap';



import { AlbumsComponent } from './albums/albums.component';
import { PlaylistsComponent } from './playlists/playlists.component';
import { AlbumComponent } from './album/album.component';
import { RecordComponent } from './record/record.component';



@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    AlbumsComponent,
    PlaylistsComponent,
    AlbumComponent,
    RecordComponent
  ],
  imports: [
    BrowserModule, SharedModule, HttpClientModule, FormsModule

    BsDropdownModule.forRoot(),
    TooltipModule.forRoot(),
    ModalModule.forRoot(),
    TabsModule.forRoot(),
    AccordionModule.forRoot()

    
  ],
  providers: [Configuration] ,
  bootstrap: [AppComponent]
})
export class AppModule { }

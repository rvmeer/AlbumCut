export class Album{
	public id: string;
	public name: string;
	public uri: string;
	public images: Image[];

	public artists: Artist[];
	public label: string;

	public record: boolean;

	constructor(
        album: Album) {
       
        this.id = album.id;
        this.name = album.name;
        this.uri = album.uri;
        this.images = album.images;
        this.artists = album.artists;
        this.label = album.label;

        this.record=false;
    }

	getSmallImageUrl(){
        return this.images.filter(i=>i.width==64)[0].url;
    } 
}

export class Image{
	public height: number;
	public width: number;
	public url: string;
}

export class Artist{
	public id: string;
	public name: string;
}

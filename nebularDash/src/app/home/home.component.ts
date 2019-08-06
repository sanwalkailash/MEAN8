import { Component, OnInit } from '@angular/core';

declare const google;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  map:any;
  marker:any;

  constructor() { }

  ngOnInit() {
  }

  ngAfterViewInit(){
    this.initialize();
  }

  initialize() {

    var myLatLng = new google.maps.LatLng(45.4375, 12.3358),
        myOptions = {
            zoom: 5,
            center: myLatLng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        this.map = new google.maps.Map(document.getElementById('map-canvas'), myOptions),
        this.marker = new google.maps.Marker({
            position: myLatLng,
            map: this.map
        });

    this.marker.setMap(this.map);
    this.moveMarker(this.map, this.marker);

}

moveMarker(map, marker) {

    //delayed so you can see it move
    setTimeout(function () {

        marker.setPosition(new google.maps.LatLng(45.4375, 12.3358));
        map.panTo(new google.maps.LatLng(45.4375, 12.3358));

    }, 1500);

};



}

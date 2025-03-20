import { Injectable } from '@angular/core';
import {ApiManagementService} from "../../../core/Services/api-management.service";

@Injectable({
  providedIn: 'root'
})
export class MusicCardService {

  constructor(private request: ApiManagementService) { }

  addTofavoriteCall(id:number){
    const data={
      sound_id:id
    }
    return this.request.post(`api/favorites/add/`, data);
  }

  deleteTofavoriteCall(id:number){
    const data={
      sound_id:id
    }
    return this.request.post(`api/favorites/remove/`, data);
  }

  buySong(id:number){
    const data={
      sound_id:id
    }
    return this.request.post(`api/buy/song/`, data);
  }
}

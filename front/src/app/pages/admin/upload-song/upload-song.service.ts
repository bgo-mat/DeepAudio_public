import { Injectable } from '@angular/core';
import {ApiManagementService} from "../../../core/Services/api-management.service";

export interface Sound {
  name: string;
  duration_seconds: number;
  bpm: number;
  key: string;
  scale: string;
  type: string[];
  subtype: string[];
  audio_file: File | string | null;
  price: string;
  is_buy:boolean,
  is_favorite:boolean
}

export interface Pack {
  name: string;
  description: string;
  total_duration: string;
  genres: string[];
  price: string;
  available_for: 'STANDARD' | 'PREMIUM';
  image: File | null;
  preview: File | string | null;
  paginated_sounds: Sound[];
}


@Injectable({
  providedIn: 'root'
})
export class UploadSongService {

  constructor(private request: ApiManagementService) {}

  uploadPack(packData: any){
    return this.request.post("api/upload_pack/", packData);
  }

  previewPack(input:any){

    const formData = new FormData();
    formData.append('file', input);

    return this.request.post(`api/preview_upload/?enable_ai_description=true&enable_ai_name=true`, formData);
  }
}

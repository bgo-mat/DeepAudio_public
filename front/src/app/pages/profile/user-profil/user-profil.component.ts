import {Component, OnInit} from '@angular/core';
import {ApiManagementService} from "../../../core/Services/api-management.service";
import {UserProfileService} from "./user-profile.service";
import {RouterLink, RouterLinkActive, RouterOutlet} from "@angular/router";

@Component({
  selector: 'app-user-profil',
  standalone: true,
    imports: [
        RouterLink,
        RouterOutlet,
        RouterLinkActive
    ],
  templateUrl: './user-profil.component.html',
  styleUrl: './user-profil.component.scss'
})
export class UserProfilComponent implements OnInit{
    constructor(private profilService: UserProfileService) {
    }

    ngOnInit() {
      this.profilService.test().subscribe(
          (data: any)=>{
              console.log("transac :",data)
          }
      )
        this.profilService.test2().subscribe(
            (data: any)=>{
                console.log("sub :", data)
            }
        )
      this.profilService.getfavoriteCall().subscribe(
          (data: any)=>{
              console.log("favoris :",data)
          }
          )
    }

}

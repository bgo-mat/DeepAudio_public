import {Injectable} from '@angular/core';
import {ApiManagementService} from "../../api-management.service";
import {Observable} from "rxjs";
import {Category} from "../../../../shared/models/category.model";


@Injectable({
  providedIn: 'root'
})
export class CategoryService {


  constructor(private apiManagementService: ApiManagementService) { }

  public getAllCategory(): Observable<Category[]> {
    return this.apiManagementService.get<Category[]>('api/genre/');
  }

  public getCategoryByID(id:number): Observable<Category[]> {
    return this.apiManagementService.get<Category[]>(`api/genre/${id}`);
  }
}

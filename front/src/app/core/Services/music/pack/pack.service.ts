import { Injectable } from '@angular/core';
import { ApiManagementService } from "../../api-management.service";
import { Observable } from "rxjs";
import { Pack } from "../../../../shared/models/pack.model";

@Injectable({
    providedIn: 'root'
})
export class PackService {
    private currentPack: Pack | null = null;

    constructor(private apiManagementService: ApiManagementService) { }

    public getPacks(ordering: string): Observable<Pack[]> {
        return this.apiManagementService.get<Pack[]>(`api/pack/?ordering=${ordering}`);
    }

    public getPackById(id: number): Observable<Pack> {
        return this.apiManagementService.get<Pack>(`api/pack/${id}`);
    }

    setPack(pack: Pack): void {
        this.currentPack = pack;
    }

    getPack(): Pack | null {
        return this.currentPack;
    }
}

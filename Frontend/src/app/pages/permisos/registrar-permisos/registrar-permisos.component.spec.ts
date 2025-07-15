import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistrarPermisosComponent } from './registrar-permisos.component';

describe('RegistrarPermisosComponent', () => {
  let component: RegistrarPermisosComponent;
  let fixture: ComponentFixture<RegistrarPermisosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegistrarPermisosComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RegistrarPermisosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

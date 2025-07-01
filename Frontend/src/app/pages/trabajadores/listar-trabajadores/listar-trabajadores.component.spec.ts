import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListarTrabajadoresComponent } from './listar-trabajadores.component';

describe('ListarTrabajadoresComponent', () => {
  let component: ListarTrabajadoresComponent;
  let fixture: ComponentFixture<ListarTrabajadoresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListarTrabajadoresComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListarTrabajadoresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

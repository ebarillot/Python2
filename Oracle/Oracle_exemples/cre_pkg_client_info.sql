set timing on

--whenever SQLERROR exit 2 rollback
set echo on
set feedb on
show user


create or replace package pkg_client_info is

procedure call_read_client_info(client_info out varchar2);

end pkg_client_info ;
/
show error


create or replace package body pkg_client_info is

procedure call_read_client_info(client_info out varchar2)
is
begin
  dbms_application_info.read_client_info(client_info=>client_info);
end call_read_client_info;

end pkg_client_info ;
/
show error

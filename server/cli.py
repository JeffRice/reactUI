import logging
from plumbum import cli
import requests
from tabulate import tabulate
from server.server import create_app
from server.calculation import Calculation
from server.calculation_machine import CalculationMachine

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")

class ServerCli(cli.Application):
    def main(self):
        pass

@ServerCli.subcommand('start')
class Start(cli.Application):
    
    other_user_freq = cli.SwitchAttr("--other-user-freq",
                                     argtype=int,
                                     default=15,
                                     help="How often, on average, simulated users should start calculations, in seconds, or -1 for never.")

    other_user_cancel_freq = cli.SwitchAttr("--other-user-cancel",
                                            argtype=int,
                                            default=90,
                                            help="How often, on average, simulated users should cancel their calculations, in seconds, or -1 for never.")

    error_freq = cli.SwitchAttr("--error-freq",
                                argtype=int,
                                default=180,
                                help="How often, on average, errors should occur, in seconds, or -1 for never")
    
    seed = cli.SwitchAttr("--seed",
                          argtype=int,
                          default=5,
                          help="Number of running calculations to seed the machine with.")

    auth = cli.Flag("--no-auth",
                    default=True,
                    help="Provide this to allow HTTP requests that do not include the"
                    " user token returned from the /login route")

    expire = cli.SwitchAttr("--expire",
                            argtype=int,
                            default=60*10,
                            help="How long completed/cancelled/errored calculations should be retined, in seconds (reclaims memory and avoids the need for pagination). -1 if they should be retained indefinitely.")
    
    @cli.positional(int)
    def main(self, port: int):

        machine = CalculationMachine()

        logging.info(f"Seeding machine with {self.seed} running calculations.")
        for _ in range(self.seed):
            machine.add(Calculation.random())
            
        if self.expire != -1:
            logging.info(f"Completed/cancelled/errored calculations will be retained {self.expire} seconds.")
            machine.start_expiration_thread(self.expire)
            
        if self.error_freq != -1:
            logging.info(f"Simulating errors roughly every {self.error_freq} seconds")
            machine.simulate_errors(frequency=self.error_freq)

        if self.other_user_cancel_freq != -1:
            logging.info(f"Simulating other users cancelling calculations roughly every {self.other_user_cancel_freq} seconds.")
            machine.simulate_cancellations(frequency=self.other_user_cancel_freq)

        if self.other_user_freq != -1:
            logging.info(f"Simulating other users starting calculations roughly every {self.other_user_freq} seconds.")
            machine.simulate_other_users(frequency=self.other_user_freq)
            
        app = create_app(machine=machine, auth=self.auth)
        app.run(port=port)
        logging.info(f"Server listening on port {port}")


@ServerCli.subcommand('list')
class List(cli.Application):
    def main(self, port):
        calcs = sorted(requests.get(f"http://127.0.0.1:{port}/calculations").json(),
                       key=lambda row: row['started_at'],
                       reverse=True)
        if not calcs:
            return
        props = ['id', 'started_at', 'cancelled_at', 'calc_type', 'foo', 'bar', 'baz', 'value', 'fraction_complete', 'completed_at']
        rows = [[calc[prop] for prop in props] for calc in calcs]
        print(tabulate(rows, headers=props))

        
if __name__ == '__main__':
    ServerCli.run()
